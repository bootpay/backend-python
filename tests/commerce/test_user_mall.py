"""Commerce API - Mall User (V1 users/...) tests."""
import pytest


class TestCommerceUserMall:
    """Commerce Mall 회원 endpoint 통합 테스트"""

    def test_uid_exist(self, commerce_client):
        """외부 uid 중복 검사"""
        response = commerce_client.user.uid_exist('nonexistent_external_uid')
        print(f"[Commerce] user.uid_exist = {response}")

        assert response is not None

    def test_user_join_check_email(self, commerce_client):
        """회원가입 중복 확인 (일반형 — email-exist)"""
        response = commerce_client.user.user_join_check('email-exist', 'nonexistent@example.com')
        print(f"[Commerce] user.user_join_check (email-exist) = {response}")

        assert response is not None

    def test_user_login_invalid(self, commerce_client):
        """잘못된 자격증명으로 회원 로그인 — 에러 응답도 응답이다"""
        response = commerce_client.user.user_login({
            'login_id': 'nonexistent_login_id',
            'password': 'wrong_password',
        })
        print(f"[Commerce] user.user_login (invalid) = {response}")

        assert response is not None

    def test_user_session_without_jwt(self, commerce_client):
        """
        JWT 없이 회원 세션 조회.

        26-08-24: 서버는 이 경우 HTTP 200 + 본문 `null` 을 돌려준다 ("세션 없음").
        SDK 는 서버 응답을 그대로 전달하므로 None 이 정상이다 —
        `is not None` 을 기대하던 기존 단정은 서버 계약과 맞지 않았다.
        """
        response = commerce_client.user.user_session()
        print(f"[Commerce] user.user_session (no jwt) = {response}")

        # 예외 없이 반환되면 된다. 세션이 없으면 None, 있으면 dict.
        assert response is None or isinstance(response, dict)
