"""PG API - request_cash_receipt wire-format tests (HTTP mock 기반)."""
from bootpay_backend.rest_client import BootpayBackend


class _Response:
    def json(self):
        return {'success': True}


def _client_with_capture(monkeypatch):
    captured = {}

    def fake_post(url, json=None, headers=None, params=None):
        captured['url'] = url
        captured['json'] = json
        return _Response()

    monkeypatch.setattr('requests.post', fake_post)
    return BootpayBackend(client_key='ck', secret_key='sk', mode='development'), captured


def test_request_cash_receipt_omits_pg_by_default(monkeypatch):
    """pg 를 넘기지 않으면 None 으로 나가 서버가 기본 PG 로 발행한다."""
    client, captured = _client_with_capture(monkeypatch)
    client.request_cash_receipt(
        order_name='테스트 현금영수증',
        identity_no='01000000000',
        purchased_at='2026-08-31T14:50:00+0900',
        price=1000,
        order_id='test_cash_001',
    )

    assert captured['url'] == 'https://dev-api.bootpay.co.kr/v2/request/cash/receipt'
    assert captured['json']['pg'] is None
    assert captured['json']['order_id'] == 'test_cash_001'
    assert captured['json']['cash_receipt_type'] == '소득공제'


def test_request_cash_receipt_sends_pg_when_given(monkeypatch):
    """pg 를 명시하면 그대로 전송한다."""
    client, captured = _client_with_capture(monkeypatch)
    client.request_cash_receipt(
        pg='나이스페이',
        order_name='테스트 현금영수증',
        identity_no='01000000000',
        purchased_at='2026-08-31T14:50:00+0900',
        price=1000,
        tax_free=0,
        user={'username': '부트페이', 'phone': '01000000000'},
        order_id='test_cash_002',
    )

    assert captured['json']['pg'] == '나이스페이'
    assert captured['json']['user'] == {'username': '부트페이', 'phone': '01000000000'}
