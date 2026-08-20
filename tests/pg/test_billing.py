"""PG API - Billing (subscription) tests."""
import pytest


class TestBilling:
    """빌링키 관련 통합 테스트"""

    def test_lookup_subscribe_billing_key_invalid(self, pg_client):
        """존재하지 않는 receipt_id로 빌링키 조회"""
        response = pg_client.lookup_subscribe_billing_key(receipt_id='invalid_receipt_id')
        print(f"[PG] lookup_subscribe_billing_key (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_lookup_billing_key_invalid(self, pg_client):
        """존재하지 않는 billing_key로 조회"""
        response = pg_client.lookup_billing_key(billing_key='invalid_billing_key')
        print(f"[PG] lookup_billing_key (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_destroy_billing_key_invalid(self, pg_client):
        """존재하지 않는 billing_key 삭제 시 에러"""
        response = pg_client.destroy_billing_key(billing_key='invalid_billing_key')
        print(f"[PG] destroy_billing_key (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_request_subscribe_billing_key_invalid_card(self, pg_client):
        """잘못된 카드 정보로 빌링키 발급 요청"""
        response = pg_client.request_subscribe_billing_key(
            pg='nicepay',
            order_name='테스트 정기결제',
            subscription_id='test_sub_001',
            card_no='0000000000000000',
            card_pw='00',
            card_identity_no='000000',
            card_expire_year='99',
            card_expire_month='12',
        )
        print(f"[PG] request_subscribe_billing_key (invalid card) = {response}")

        assert response is not None
        # 잘못된 카드이므로 에러 예상
        assert 'error_code' in response

    def test_request_subscribe_payment_invalid(self, pg_client):
        """존재하지 않는 billing_key로 정기결제 실행"""
        response = pg_client.request_subscribe_payment(
            billing_key='invalid_billing_key',
            order_name='테스트 결제',
            price=1000,
            order_id='test_order_001',
        )
        print(f"[PG] request_subscribe_payment (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_subscribe_payment_reserve_invalid(self, pg_client):
        """존재하지 않는 billing_key로 예약 결제"""
        response = pg_client.subscribe_payment_reserve(
            billing_key='invalid_billing_key',
            order_name='테스트 예약결제',
            price=1000,
            order_id='test_reserve_001',
            reserve_execute_at='2099-12-31T00:00:00+09:00',
        )
        print(f"[PG] subscribe_payment_reserve (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_subscribe_payment_reserve_lookup_invalid(self, pg_client):
        """존재하지 않는 reserve_id로 예약 결제 조회"""
        response = pg_client.subscribe_payment_reserve_lookup(reserve_id='invalid_reserve_id')
        print(f"[PG] subscribe_payment_reserve_lookup (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_cancel_subscribe_reserve_invalid(self, pg_client):
        """존재하지 않는 reserve_id로 예약 결제 취소"""
        response = pg_client.cancel_subscribe_reserve(reserve_id='invalid_reserve_id')
        print(f"[PG] cancel_subscribe_reserve (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response
