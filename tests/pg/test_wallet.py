"""PG API - Wallet tests."""
import pytest


class TestWallet:
    """지갑 관련 통합 테스트"""

    def test_get_user_wallets(self, pg_client):
        """사용자 지갑 목록 조회"""
        response = pg_client.get_user_wallets(user_id='test_user_001', sandbox=True)
        print(f"[PG] get_user_wallets = {response}")

        assert response is not None

    def test_get_user_wallets_invalid_user(self, pg_client):
        """존재하지 않는 사용자의 지갑 조회"""
        response = pg_client.get_user_wallets(user_id='nonexistent_user', sandbox=True)
        print(f"[PG] get_user_wallets (invalid user) = {response}")

        assert response is not None

    def test_request_wallet_payment_invalid(self, pg_client):
        """잘못된 데이터로 지갑 결제 요청"""
        response = pg_client.request_wallet_payment(
            user_id='test_user_001',
            order_name='테스트 지갑결제',
            price=1000,
            order_id='test_wallet_001',
            sandbox=True,
        )
        print(f"[PG] request_wallet_payment (invalid) = {response}")

        assert response is not None
