"""Commerce API - Token tests."""
import pytest
from bootpay_backend.commerce import BootpayCommerce
from tests.conftest import COMMERCE_KEYS, _get_env


class TestCommerceToken:
    """Commerce get_access_token 통합 테스트"""

    def test_commerce_token_exists(self, commerce_client):
        """commerce_client fixture에 토큰이 설정되어 있는지 확인"""
        assert commerce_client.has_token()
        print(f"[Commerce] token exists = {commerce_client.has_token()}")

    def test_commerce_get_access_token(self):
        """새 클라이언트로 토큰 발급 후 응답 구조 확인"""
        env = _get_env()
        keys = COMMERCE_KEYS[env]
        client = BootpayCommerce(
            client_key=keys['client_key'],
            secret_key=keys['secret_key'],
            mode=env,
        )
        response = client.get_access_token()
        print(f"[Commerce] get_access_token response = {response}")

        assert response is not None
        assert 'access_token' in response
        assert client.has_token()

    def test_commerce_token_invalid_key(self):
        """잘못된 키로 토큰 발급 시 에러 반환"""
        env = _get_env()
        client = BootpayCommerce(
            client_key='invalid_client_key',
            secret_key='invalid_secret_key',
            mode=env,
        )
        response = client.get_access_token()
        print(f"[Commerce] invalid key response = {response}")

        assert response is not None
        assert not client.has_token()

    def test_commerce_with_token_chaining(self):
        """with_token() 메서드 체이닝 확인"""
        env = _get_env()
        keys = COMMERCE_KEYS[env]
        client = BootpayCommerce(
            client_key=keys['client_key'],
            secret_key=keys['secret_key'],
            mode=env,
        )
        result = client.with_token()
        print(f"[Commerce] with_token() chaining = {result}")

        assert result is client
        assert client.has_token()
