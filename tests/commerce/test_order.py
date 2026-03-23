"""Commerce API - Order tests."""
import pytest


class TestCommerceOrder:
    """Commerce Order 모듈 통합 테스트"""

    def test_order_list(self, commerce_client):
        """주문 목록 조회"""
        response = commerce_client.order.list({'page': 1, 'limit': 10})
        print(f"[Commerce] order.list = {response}")

        assert response is not None

    def test_order_list_with_filters(self, commerce_client):
        """필터 조건으로 주문 목록 조회"""
        response = commerce_client.order.list({
            'page': 1,
            'limit': 5,
            'keyword': 'test',
        })
        print(f"[Commerce] order.list (filtered) = {response}")

        assert response is not None

    def test_order_detail_invalid(self, commerce_client):
        """존재하지 않는 주문 상세 조회"""
        response = commerce_client.order.detail(order_id='nonexistent_order_id')
        print(f"[Commerce] order.detail (invalid) = {response}")

        assert response is not None

    def test_order_cancel_list(self, commerce_client):
        """주문 취소 목록 조회"""
        response = commerce_client.order_cancel.list({})
        print(f"[Commerce] order_cancel.list = {response}")

        assert response is not None

    def test_order_subscription_list(self, commerce_client):
        """정기구독 목록 조회"""
        response = commerce_client.order_subscription.list({'page': 1, 'limit': 10})
        print(f"[Commerce] order_subscription.list = {response}")

        assert response is not None

    def test_order_subscription_detail_invalid(self, commerce_client):
        """존재하지 않는 정기구독 상세 조회"""
        response = commerce_client.order_subscription.detail(
            order_subscription_id='nonexistent_id',
        )
        print(f"[Commerce] order_subscription.detail (invalid) = {response}")

        assert response is not None

    def test_order_subscription_bill_list(self, commerce_client):
        """정기구독 청구 목록 조회"""
        response = commerce_client.order_subscription_bill.list({'page': 1, 'limit': 10})
        print(f"[Commerce] order_subscription_bill.list = {response}")

        assert response is not None
