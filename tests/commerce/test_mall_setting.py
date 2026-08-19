"""Commerce API - MallSetting tests."""
import pytest


class TestCommerceMallSetting:
    """Commerce MallSetting 모듈 통합 테스트 (supervisor scope 전용)"""

    def test_mall_setting_detail(self, commerce_client):
        """몰 설정 조회"""
        response = commerce_client.mall_setting.get_mall_setting()
        print(f"[Commerce] mall_setting.get_mall_setting = {response}")

        assert response is not None

    def test_mall_setting_detail_alias(self, commerce_client):
        """detail 별칭도 같은 endpoint 를 부른다"""
        response = commerce_client.mall_setting.detail()
        print(f"[Commerce] mall_setting.detail = {response}")

        assert response is not None
