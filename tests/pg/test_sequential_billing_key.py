"""PG API - lookup_sequential_billing_key wire-format tests (HTTP mock 기반)."""
from bootpay_backend.rest_client import BootpayBackend


class _Response:
    def json(self):
        return {'success': True}


def test_lookup_sequential_billing_key_url_and_encoding(monkeypatch):
    captured = {}

    def fake_get(url, headers=None, params=None):
        captured['url'] = url
        return _Response()

    monkeypatch.setattr('requests.get', fake_get)

    client = BootpayBackend(client_key='ck', secret_key='sk', mode='development')
    client.lookup_sequential_billing_key(
        widget_key='widget key/1',
        billing_key='BK123',
        user_id='user@1',
    )

    assert captured['url'] == (
        'https://dev-api.bootpay.co.kr/v2/subscribe/sequential_billing_key/BK123'
        '?widget_key=widget%20key%2F1&user_id=user%401'
    )
