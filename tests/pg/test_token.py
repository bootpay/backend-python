"""PG API - Token tests."""
import pytest
from bootpay_backend.rest_client import BootpayBackend
from tests.conftest import PG_KEYS, _get_env


class TestGetAccessToken:
    """get_access_token 통합 테스트"""

    def test_get_access_token_success(self, pg_client):
        """토큰이 이미 발급된 pg_client fixture를 통해 토큰 존재 확인"""
        assert pg_client.token is not None
        print(f"[PG] access_token = {pg_client.token}")

    def test_get_access_token_returns_token(self):
        """새 클라이언트로 토큰 발급 후 응답 구조 확인"""
        env = _get_env()
        keys = PG_KEYS[env]
        client = BootpayBackend(
            application_id=keys['application_id'],
            private_key=keys['private_key'],
            mode=env,
        )
        response = client.get_access_token()
        print(f"[PG] get_access_token response = {response}")

        assert response is not None
        assert 'error_code' not in response
        assert 'access_token' in response

    def test_get_access_token_invalid_key(self):
        """잘못된 키로 토큰 발급 시 에러 반환"""
        env = _get_env()
        client = BootpayBackend(
            application_id='invalid_app_id',
            private_key='invalid_private_key',
            mode=env,
        )
        response = client.get_access_token()
        print(f"[PG] invalid key response = {response}")

        assert response is not None
        assert 'error_code' in response
