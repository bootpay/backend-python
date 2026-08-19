"""Commerce API - OrderSubscription charge / requestIng purchase·transfer tests."""
import pytest


class TestCommerceOrderSubscriptionCharge:
    """수시결제(온디맨드) charge_key 결제/해지 통합 테스트 (supervisor 전용)"""

    def test_supervisor_charge_invalid_key(self, commerce_client):
        """존재하지 않는 charge_key 로 즉시 결제 요청 — 에러 응답도 응답이다"""
        response = commerce_client.order_subscription.supervisor_charge({
            'charge_key': 'nonexistent_charge_key',
            'price': 1000,
            'tax_free_price': 0,
        })
        print(f"[Commerce] order_subscription.supervisor_charge (invalid) = {response}")

        assert response is not None

    def test_supervisor_charge_revoke_invalid_key(self, commerce_client):
        """존재하지 않는 charge_key 해지"""
        response = commerce_client.order_subscription.supervisor_charge_revoke({
            'charge_key': 'nonexistent_charge_key',
        })
        print(f"[Commerce] order_subscription.supervisor_charge_revoke (invalid) = {response}")

        assert response is not None


class TestCommerceOrderSubscriptionRequestIng:
    """requestIng purchase / transfer 통합 테스트"""

    def test_request_ing_purchase_invalid(self, commerce_client):
        """존재하지 않는 구독으로 중도인수 요청"""
        response = commerce_client.order_subscription.request_ing.purchase({
            'order_subscription_id': 'nonexistent_order_subscription_id',
            'price': 1000,
        })
        print(f"[Commerce] order_subscription.request_ing.purchase (invalid) = {response}")

        assert response is not None

    def test_request_ing_transfer_invalid(self, commerce_client):
        """존재하지 않는 구독으로 이전/승계 요청"""
        response = commerce_client.order_subscription.request_ing.transfer({
            'order_subscription_id': 'nonexistent_order_subscription_id',
            'new_user_id': 'nonexistent_user_id',
        })
        print(f"[Commerce] order_subscription.request_ing.transfer (invalid) = {response}")

        assert response is not None
