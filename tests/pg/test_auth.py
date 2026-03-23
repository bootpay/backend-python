"""PG API - Authentication (identity verification) tests."""
import pytest


class TestAuthentication:
    """본인인증 관련 통합 테스트"""

    def test_certificate_invalid(self, pg_client):
        """존재하지 않는 receipt_id로 인증 데이터 조회"""
        response = pg_client.certificate(receipt_id='invalid_receipt_id')
        print(f"[PG] certificate (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_request_authentication(self, pg_client):
        """본인인증 요청 (테스트 데이터)"""
        response = pg_client.request_authentication(
            pg='danal',
            method='sms',
            username='홍길동',
            identity_no='900101',
            carrier='SKT',
            phone='01012345678',
            site_url='https://test.bootpay.co.kr',
            order_name='테스트 본인인증',
            authentication_id='test_auth_001',
            authenticate_type='sms',
            client_ip='127.0.0.1',
        )
        print(f"[PG] request_authentication = {response}")

        assert response is not None

    def test_confirm_authentication_invalid(self, pg_client):
        """존재하지 않는 receipt_id로 본인인증 승인"""
        response = pg_client.confirm_authentication(
            receipt_id='invalid_receipt_id',
            otp='123456',
        )
        print(f"[PG] confirm_authentication (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_realarm_authentication_invalid(self, pg_client):
        """존재하지 않는 receipt_id로 SMS 재발송"""
        response = pg_client.realarm_authentication(receipt_id='invalid_receipt_id')
        print(f"[PG] realarm_authentication (invalid) = {response}")

        assert response is not None
        assert 'error_code' in response

    def test_request_user_token(self, pg_client):
        """사용자 토큰 발급"""
        response = pg_client.request_user_token(
            user_id='test_user_001',
            email='test@bootpay.co.kr',
            username='테스트유저',
            gender=1,
            birth='19900101',
            phone='01012345678',
        )
        print(f"[PG] request_user_token = {response}")

        assert response is not None
        assert 'error_code' not in response
        assert 'user_token' in response
