"""Commerce API - Store tests."""
import pytest


class TestCommerceStore:
    """Commerce Store 모듈 통합 테스트"""

    def test_store_info(self, commerce_client):
        """가맹점 기본 정보 조회"""
        response = commerce_client.store.info()
        print(f"[Commerce] store.info = {response}")

        assert response is not None

    def test_store_detail(self, commerce_client):
        """가맹점 상세 정보 조회"""
        response = commerce_client.store.detail()
        print(f"[Commerce] store.detail = {response}")

        assert response is not None
