"""PG API - Cash receipt tests."""
import pytest


class TestCashReceipt:
    """현금영수증 관련 통합 테스트"""

    def test_cash_receipt_publish_on_receipt_invalid(self, pg_client):
        """존재하지 않는 receipt_id로 현금영수증 발행"""
        response = pg_client.cash_receipt_publish_on_receipt(
            receipt_id='invalid_receipt_id',
            username='테스트',
            email='test@bootpay.co.kr',
            phone='01012345678',
            identity_no='0101010000000',
            cash_receipt_type='소득공제',
        )
        print(f"[PG] cash_receipt_publish_on_receipt (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_cash_receipt_cancel_on_receipt_invalid(self, pg_client):
        """존재하지 않는 receipt_id로 현금영수증 취소"""
        response = pg_client.cash_receipt_cancel_on_receipt(
            receipt_id='invalid_receipt_id',
            cancel_username='시스템',
            cancel_message='테스트 취소',
        )
        print(f"[PG] cash_receipt_cancel_on_receipt (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_request_cash_receipt_invalid(self, pg_client):
        """잘못된 데이터로 현금영수증 별건 발행"""
        response = pg_client.request_cash_receipt(
            pg='nicepay',
            order_name='테스트 현금영수증',
            identity_no='0101010000000',
            cash_receipt_type='소득공제',
            price=1000,
            order_id='test_cash_001',
        )
        print(f"[PG] request_cash_receipt = {response}")

        assert response is not None

    def test_cancel_cash_receipt_invalid(self, pg_client):
        """존재하지 않는 receipt_id로 현금영수증 별건 취소"""
        response = pg_client.cancel_cash_receipt(
            receipt_id='invalid_receipt_id',
            cancel_username='시스템',
            cancel_message='테스트 취소',
        )
        print(f"[PG] cancel_cash_receipt (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response
