"""Commerce API - Webhook tests."""
import pytest


class TestCommerceWebhook:
    """Commerce Webhook 모듈 통합 테스트"""

    def test_webhook_send_test(self, commerce_client):
        """테스트 웹훅 발송 (header_content_type 미지정 — 서버 기본값)"""
        response = commerce_client.webhook.send_test()
        print(f"[Commerce] webhook.send_test = {response}")

        assert response is not None

    def test_webhook_send_test_with_content_type(self, commerce_client):
        """Content-Type 지정 발송"""
        response = commerce_client.webhook.send_test({'header_content_type': 1})
        print(f"[Commerce] webhook.send_test (content-type) = {response}")

        assert response is not None
