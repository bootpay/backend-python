"""PG API - Token tests."""
import pytest
from bootpay_backend.rest_client import BootpayBackend
from tests.conftest import PG_KEYS, PG_LEGACY_KEYS, _get_env

# 라이브 API 게이트 — fixture 를 거치지 않고 직접 클라이언트를 만들어 실제 API 를 호출하므로
# BOOTPAY_ENV=development 일 때만 실행한다 (무인자 실행의 production 호출 방지).
pytestmark = pytest.mark.skipif(
    _get_env() != 'development',
    reason='live API tests run only with BOOTPAY_ENV=development',
)


class TestGetAccessToken:
    """get_access_token 통합 테스트"""

    def test_get_access_token_ck_sk_returns_synthetic(self):
        """ck/sk 모드: HTTP 호출 없이 합성 응답 ({access_token: '', expire_in: 0}) 반환."""
        env = _get_env()
        keys = PG_KEYS[env]
        client = BootpayBackend(
            client_key=keys['client_key'],
            secret_key=keys['secret_key'],
            mode=env,
        )
        response = client.get_access_token()
        print(f"[PG][ck/sk] response = {response}")

        assert response == {'access_token': '', 'expire_in': 0}
        assert client.token == ''

    def test_get_access_token_legacy_issues_real_token(self):
        """legacy application_id/private_key 모드: request/token 호출 후 실제 토큰 발급."""
        env = _get_env()
        legacy = PG_LEGACY_KEYS[env]
        client = BootpayBackend(
            application_id=legacy['application_id'],
            private_key=legacy['private_key'],
            mode=env,
        )
        response = client.get_access_token()
        print(f"[PG][legacy] response = {response}")

        assert response is not None
        assert 'error_code' not in response, f"legacy token failed: {response}"
        assert response.get('access_token'), "access_token must not be empty"
        assert response.get('expire_in', 0) > 0
        assert client.token == response['access_token']

    def test_get_access_token_invalid_legacy_key(self):
        """잘못된 legacy 키로 토큰 발급 시 에러 반환."""
        env = _get_env()
        client = BootpayBackend(
            application_id='invalid_application_id',
            private_key='invalid_private_key',
            mode=env,
        )
        response = client.get_access_token()
        print(f"[PG][legacy invalid] response = {response}")

        assert response is not None
        assert 'error_code' in response
