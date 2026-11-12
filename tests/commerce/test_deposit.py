"""뱅크알람 입금대기 wire-format 계약 (HTTP mock, 네트워크 불필요)."""
from copy import deepcopy
from uuid import UUID

import pytest

from bootpay_backend.commerce import BootpayCommerce


class _Response:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


@pytest.fixture
def commerce():
    return BootpayCommerce(client_key='ck', secret_key='sk', mode='development').as_manager()


@pytest.fixture
def captured(monkeypatch):
    box = {'response': {'success': True}}

    def _capture(method):
        def fake(url, headers=None, params=None, json=None, timeout=None):
            box.update(method=method, url=url, headers=headers or {}, params=params, json=json)
            return _Response(box['response'])
        return fake

    for method in ('get', 'post', 'delete'):
        monkeypatch.setattr('requests.' + method, _capture(method))
    return box


ROUTES = [
    ('accounts', lambda c: c.deposit.accounts(), 'get', 'sdk/deposits/accounts'),
    ('webhook_secret', lambda c: c.deposit.webhook_secret(), 'post', 'sdk/deposits/webhook_secret'),
    ('create', lambda c: c.deposit.create({'merchant_order_id': 'm-1', 'price': 15000, 'depositor': '홍길동'}),
     'post', 'sdk/deposits'),
    ('detail', lambda c: c.deposit.detail('m-1'), 'get', 'sdk/deposits/m-1'),
    ('cancel', lambda c: c.deposit.cancel('m-1'), 'delete', 'sdk/deposits/m-1'),
]


@pytest.mark.parametrize('label,call,method,path', ROUTES, ids=[row[0] for row in ROUTES])
def test_deposit_routes_scope_and_fresh_uuid(commerce, captured, label, call, method, path):
    response = call(commerce)
    assert response is captured['response']
    assert captured['method'] == method
    assert captured['url'] == 'https://dev-api.bootapi.com/v1/' + path
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'
    assert commerce.get_current_role() == 'manager'
    first_key = captured['headers']['Idempotency-Key']
    assert UUID(first_key).version == 4

    call(commerce)
    second_key = captured['headers']['Idempotency-Key']
    assert UUID(second_key).version == 4
    assert first_key != second_key
    assert commerce.get_current_role() == 'manager'


@pytest.mark.parametrize('method', ['detail', 'cancel'])
@pytest.mark.parametrize('deposit_id,encoded', [
    ('a/b', 'a%2Fb'),
    ('주문 ?#%+', '%EC%A3%BC%EB%AC%B8%20%3F%23%25%2B'),
])
def test_deposit_id_is_one_encoded_segment(commerce, captured, method, deposit_id, encoded):
    getattr(commerce.deposit, method)(deposit_id)
    assert captured['url'] == 'https://dev-api.bootapi.com/v1/sdk/deposits/' + encoded


@pytest.mark.parametrize('method', ['create', 'webhook_secret', 'cancel'])
def test_deposit_explicit_idempotency_key(commerce, captured, method):
    if method == 'create':
        commerce.deposit.create({
            'merchant_order_id': 'm-1', 'price': 15000, 'depositor': '홍길동',
            'idempotency_key': 'deposit-key',
        })
        assert 'idempotency_key' not in captured['json']
    elif method == 'cancel':
        commerce.deposit.cancel('m-1', idempotency_key='deposit-key')
    else:
        commerce.deposit.webhook_secret(idempotency_key='deposit-key')
    assert captured['headers']['Idempotency-Key'] == 'deposit-key'


def test_deposit_webhook_secret_posts_empty_object(commerce, captured):
    commerce.deposit.webhook_secret()
    assert captured['json'] == {}


def test_deposit_create_compacts_none_and_preserves_false_without_mutation(commerce, captured):
    params = {
        'merchant_order_id': 'm-1', 'price': 15000, 'depositor': '홍길동',
        'order_name': '주문', 'memo': None, 'buyer_name': None,
        'buyer_phone': '01012345678', 'buyer_email': None, 'account_id': 'acc1',
        'webhook_url': 'https://example.com/hooks/deposit', 'idempotency_key': None,
        'notify': {'deposit_guide': True, 'deposit_paid': False, 'link': None},
    }
    original = deepcopy(params)
    commerce.deposit.create(params)
    assert captured['json'] == {
        'merchant_order_id': 'm-1', 'price': 15000, 'depositor': '홍길동',
        'order_name': '주문', 'buyer_phone': '01012345678', 'account_id': 'acc1',
        'webhook_url': 'https://example.com/hooks/deposit',
        'notify': {'deposit_guide': True, 'deposit_paid': False},
    }
    assert params == original


def test_deposit_create_preserves_all_optional_fields(commerce, captured):
    params = {
        'merchant_order_id': 'm-1', 'price': 15000, 'depositor': '홍길동',
        'order_name': '주문', 'memo': '메모', 'buyer_name': '구매자',
        'buyer_phone': '01012345678', 'buyer_email': 'buyer@example.com', 'account_id': 'acc1',
        'webhook_url': 'https://example.com/hooks/deposit',
        'notify': {'deposit_guide': False, 'deposit_paid': False, 'link': 'https://example.com/m-1'},
    }
    commerce.deposit.create(params)
    assert captured['json'] == params


def test_deposit_create_omits_none_notify(commerce, captured):
    commerce.deposit.create({'merchant_order_id': 'm-1', 'price': 15000, 'depositor': '홍길동', 'notify': None})
    assert captured['json'] == {'merchant_order_id': 'm-1', 'price': 15000, 'depositor': '홍길동'}


def test_deposit_event_constants_are_public():
    import bootpay_backend.commerce as commerce

    events = ['RECEIVED', 'MATCHED', 'AMBIGUOUS', 'UNMATCHED',
              'CONFIRMED_MANUALLY', 'EXPIRED', 'CANCELLED', 'REVERTED']
    names = ['BANK_DEPOSIT_WEBHOOK_EVENT_' + event for event in events]
    assert [getattr(commerce, name) for name in names] == list(range(400, 408))
    assert all(name in commerce.__all__ for name in names)


@pytest.mark.parametrize('call', [
    lambda commerce: commerce.deposit.detail(''),
    lambda commerce: commerce.deposit.cancel(''),
])
def test_deposit_empty_id_is_rejected_before_request(commerce, captured, call):
    # 빈 id 는 상위 경로(sdk/deposits/)를 때린다 — 다른 커머스 모듈처럼 요청 전에 막는다
    with pytest.raises(ValueError):
        call(commerce)
    assert 'method' not in captured
