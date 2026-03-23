"""PG API - Payment tests."""
import pytest


class TestReceiptPayment:
    """receipt_payment / confirm_payment / cancel_payment 통합 테스트"""

    def test_receipt_payment_with_invalid_id(self, pg_client):
        """존재하지 않는 receipt_id로 조회 시 에러 반환"""
        response = pg_client.receipt_payment(receipt_id='invalid_receipt_id')
        print(f"[PG] receipt_payment (invalid) = {response}")

        assert response is not None
        # 잘못된 ID이므로 에러가 반환되어야 함
        assert 'error_code' in response

    def test_confirm_payment_with_invalid_id(self, pg_client):
        """존재하지 않는 receipt_id로 결제 승인 시 에러 반환"""
        response = pg_client.confirm_payment(receipt_id='invalid_receipt_id')
        print(f"[PG] confirm_payment (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_cancel_payment_with_invalid_id(self, pg_client):
        """존재하지 않는 receipt_id로 결제 취소 시 에러 반환"""
        response = pg_client.cancel_payment(
            receipt_id='invalid_receipt_id',
            cancel_username='test',
            cancel_message='integration test cancel',
        )
        print(f"[PG] cancel_payment (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_receipt_payment_with_lookup_user_data(self, pg_client):
        """lookup_user_data 파라미터 포함 조회"""
        response = pg_client.receipt_payment(
            receipt_id='invalid_receipt_id',
            lookup_user_data=True,
        )
        print(f"[PG] receipt_payment (lookup_user_data) = {response}")

        assert response is not None
