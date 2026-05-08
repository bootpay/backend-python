"""PG API - legacy application_id/private_key compatibility tests."""
import base64

from bootpay_backend.rest_client import BootpayBackend


def test_legacy_constructor_keeps_application_credentials():
    client = BootpayBackend(
        application_id='legacy_application_id',
        private_key='legacy_private_key',
        mode='development',
    )

    assert client.application_id == 'legacy_application_id'
    assert client.private_key == 'legacy_private_key'
    assert client.client_key is None
    assert client.secret_key is None
    assert client.mode == 'development'


def test_legacy_authorization_uses_bearer_token_when_present():
    client = BootpayBackend(application_id='legacy_application_id', private_key='legacy_private_key')
    client.token = 'legacy_access_token'

    assert client._BootpayBackend__authorization() == 'Bearer legacy_access_token'


def test_legacy_token_request_omits_authorization_header(monkeypatch):
    captured = {}

    class Response:
        def json(self):
            return {'access_token': 'legacy_access_token'}

    def fake_post(url, json=None, headers=None, params=None):
        captured['url'] = url
        captured['json'] = json
        captured['headers'] = headers
        return Response()

    monkeypatch.setattr('requests.post', fake_post)

    client = BootpayBackend(application_id='legacy_application_id', private_key='legacy_private_key')
    response = client.get_access_token()

    assert response == {'access_token': 'legacy_access_token'}
    assert captured['json'] == {
        'application_id': 'legacy_application_id',
        'private_key': 'legacy_private_key',
    }
    assert 'Authorization' not in captured['headers']


def test_client_key_get_access_token_is_synthetic_no_http(monkeypatch):
    """ck/sk 모드의 get_access_token 은 Option A 로 HTTP 호출 없이 합성 응답만 돌려준다."""
    called = {'count': 0}

    def fake_post(url, json=None, headers=None, params=None):
        called['count'] += 1
        raise AssertionError('ck/sk get_access_token 은 HTTP 호출을 발생시키면 안 된다')

    monkeypatch.setattr('requests.post', fake_post)

    client = BootpayBackend(client_key='ck', secret_key='sk')
    response = client.get_access_token()

    assert response == {'access_token': '', 'expire_in': 0}
    assert called['count'] == 0
    assert client.token == ''


def test_client_key_subsequent_request_uses_basic_authorization(monkeypatch):
    """ck/sk 모드에서 후속 API 호출은 매 요청 Basic Auth 헤더를 부착한다."""
    captured = {}

    class Response:
        def json(self):
            return {'success': True}

    def fake_get(url, headers=None, params=None):
        captured['headers'] = headers
        return Response()

    monkeypatch.setattr('requests.get', fake_get)

    client = BootpayBackend(client_key='ck', secret_key='sk')
    client.receipt_payment(receipt_id='test_receipt')

    expected = 'Basic ' + base64.b64encode(b'ck:sk').decode('utf-8')
    assert captured['headers']['Authorization'] == expected
