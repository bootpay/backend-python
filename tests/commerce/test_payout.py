"""입점사 지급 요청 wire-format 계약 (HTTP mock, 네트워크 불필요)."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
from typing import get_args
from uuid import UUID

import pytest
import requests

import bootpay_backend.commerce as commerce_exports
from bootpay_backend.commerce import BootpayCommerce
from bootpay_backend.commerce.modules import PayoutModule
from bootpay_backend.commerce.types import PayoutStatus


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
            return box['response'] if isinstance(box['response'], requests.Response) else _Response(box['response'])
        return fake

    monkeypatch.setattr('requests.get', _capture('get'))
    monkeypatch.setattr('requests.post', _capture('post'))
    return box


ROUTES = [
    ('create', lambda c: c.payout.create({
        'sub_seller_id': 'seller-1', 'amount': 150000, 'merchant_payout_id': 'payout-1'
    }), 'post', 'sdk/payouts'),
    ('detail', lambda c: c.payout.detail('payout-1'), 'get', 'sdk/payouts/payout-1'),
    ('list', lambda c: c.payout.list(), 'get', 'sdk/payouts'),
]


@pytest.mark.parametrize('label,call,method,path', ROUTES, ids=[row[0] for row in ROUTES])
def test_payout_routes_scope_and_fresh_uuid(commerce, captured, label, call, method, path):
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


def test_payout_detail_encodes_id_as_one_path_segment(commerce, captured):
    commerce.payout.detail('a/b c?d#e한')
    assert captured['url'] == (
        'https://dev-api.bootapi.com/v1/sdk/payouts/'
        'a%2Fb%20c%3Fd%23e%ED%95%9C'
    )


def test_payout_empty_id_is_rejected_before_request(commerce, captured):
    with pytest.raises(ValueError, match='payout_id is required'):
        commerce.payout.detail('')
    assert 'method' not in captured


@pytest.mark.parametrize('method', ['create', 'detail', 'list'])
def test_payout_explicit_idempotency_key(commerce, captured, method):
    if method == 'create':
        commerce.payout.create({
            'sub_seller_id': 'seller-1', 'amount': 150000,
            'merchant_payout_id': 'payout-1', 'idempotency_key': 'payout-key',
        })
        assert 'idempotency_key' not in captured['json']
    elif method == 'detail':
        commerce.payout.detail('payout-1', idempotency_key='payout-key')
    else:
        commerce.payout.list({'idempotency_key': 'payout-key'})
        assert 'idempotency_key' not in captured['params']
    assert captured['headers']['Idempotency-Key'] == 'payout-key'


def test_payout_create_compacts_none_and_does_not_mutate_input(commerce, captured):
    params = {
        'sub_seller_id': 'seller-1', 'amount': 150000, 'merchant_payout_id': 'payout-1',
        'order_number': None, 'payout_date': '2026-11-20', 'idempotency_key': None,
    }
    original = deepcopy(params)
    commerce.payout.create(params)
    assert captured['json'] == {
        'sub_seller_id': 'seller-1', 'amount': 150000,
        'merchant_payout_id': 'payout-1', 'payout_date': '2026-11-20',
    }
    assert params == original


def test_payout_list_forwards_filters_omits_none_and_injects_no_defaults(commerce, captured):
    params = {
        'status': 'ready', 'sub_seller_id': 'seller-1',
        'from': '2026-11-01', 'to': '2026-11-30',
        'page': 2, 'limit': 50, 'idempotency_key': None,
        'unused': None,
    }
    original = deepcopy(params)
    commerce.payout.list(params)
    assert captured['params'] == {
        'status': 'ready', 'sub_seller_id': 'seller-1',
        'from': '2026-11-01', 'to': '2026-11-30', 'page': 2, 'limit': 50,
    }
    assert params == original

    commerce.payout.list()
    assert captured['params'] == {}
    commerce.payout.list(None)
    assert captured['params'] == {}


def test_payout_list_decodes_bare_json_array_and_preserves_nullable_fields(commerce, captured):
    items = [{
        'id': 'payout-id', 'merchant_payout_id': 'payout-1', 'sub_seller_id': 'seller-1',
        'amount': 150000, 'status': 'ready', 'payout_date': '2026-11-20',
        'order_number': None, 'last_code': None, 'last_message': None,
        'created_at': '2026-11-12T00:00:00+09:00', 'updated_at': '2026-11-12T00:00:00+09:00',
    }]
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(items).encode('utf-8')
    captured['response'] = response

    assert commerce.payout.list() == items


def test_payout_public_entry_surfaces_and_statuses(commerce):
    assert isinstance(commerce.payout, PayoutModule)
    assert commerce_exports.PayoutModule is PayoutModule
    for name in ('PayoutStatus', 'PayoutCreateParams', 'PayoutListParams', 'CommercePayout'):
        assert name in commerce_exports.__all__
    assert set(get_args(PayoutStatus)) == {
        'ready', 'held', 'sending', 'requested', 'processing',
        'succeeded', 'failed', 'cancelled', 'unknown', 'void',
    }


def test_payout_live_guard_defaults_to_off(monkeypatch, capsys):
    monkeypatch.setenv('BOOTPAY_TEST_PAYOUT_LIVE', 'false')
    config_path = Path(__file__).parents[2] / 'test' / 'config.py'
    spec = importlib.util.spec_from_file_location('payout_test_config', config_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.payout_side_effect_allowed('payout_create') is False
    assert 'BOOTPAY_TEST_PAYOUT_LIVE=true' in capsys.readouterr().out


@pytest.mark.parametrize('filename', ['payout_create.py', 'payout_detail.py', 'payout_list.py'])
def test_payout_examples_guard_before_client_or_network(filename):
    source = (Path(__file__).parents[2] / 'test' / 'commerce' / filename).read_text(encoding='utf-8')
    guard = "if not payout_side_effect_allowed("
    assert source.index(guard) < source.index('commerce = BootpayCommerce(')
