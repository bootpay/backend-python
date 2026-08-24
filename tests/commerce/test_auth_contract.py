"""Commerce API authentication contract tests without live requests."""
import base64

import pytest

from bootpay_backend.commerce import BootpayCommerce


def test_commerce_request_uses_complete_client_key_pair(monkeypatch):
    captured = {}

    class Response:
        def json(self):
            return {'success': True}

    def fake_get(url, headers=None, params=None, timeout=None):
        captured['headers'] = headers
        return Response()

    monkeypatch.setattr('requests.get', fake_get)
    client = BootpayCommerce(client_key='ck', secret_key='sk')
    client.get('users')

    expected = 'Basic ' + base64.b64encode(b'ck:sk').decode()
    assert captured['headers']['Authorization'] == expected


def test_stored_commerce_token_never_replaces_basic_auth(monkeypatch):
    captured = {}

    class Response:
        def json(self):
            return {'success': True}

    def fake_get(url, headers=None, params=None, timeout=None):
        captured['headers'] = headers
        return Response()

    monkeypatch.setattr('requests.get', fake_get)
    client = BootpayCommerce(client_key='ck', secret_key='sk')
    client.set_token('stored_access_token')
    client.get('users')

    expected = 'Basic ' + base64.b64encode(b'ck:sk').decode()
    assert captured['headers']['Authorization'] == expected
    assert captured['headers']['Authorization'] != 'Bearer stored_access_token'


@pytest.mark.parametrize(
    'credentials, missing_name',
    [
        ({'client_key': 'ck'}, 'secret_key'),
        ({'secret_key': 'sk'}, 'client_key'),
        ({}, 'client_key와 secret_key'),
    ],
)
def test_invalid_commerce_credentials_fail_before_network(monkeypatch, credentials, missing_name):
    called = {'count': 0}

    def fake_get(*args, **kwargs):
        called['count'] += 1
        raise AssertionError('잘못된 Commerce 인증 정보로 네트워크 요청을 보내면 안 된다')

    monkeypatch.setattr('requests.get', fake_get)
    client = BootpayCommerce(**credentials)

    with pytest.raises(ValueError, match=missing_name):
        client.get('users')

    assert called['count'] == 0


def test_commerce_token_request_rejects_partial_pair_before_network(monkeypatch):
    called = {'count': 0}

    def fake_post(*args, **kwargs):
        called['count'] += 1
        raise AssertionError('부분 인증 정보로 토큰 요청을 보내면 안 된다')

    monkeypatch.setattr('requests.post', fake_post)
    client = BootpayCommerce(client_key='ck')

    with pytest.raises(ValueError, match='secret_key'):
        client.get_access_token()

    assert called['count'] == 0
