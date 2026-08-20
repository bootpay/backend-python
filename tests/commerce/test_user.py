"""Commerce API - User tests."""
import pytest
import uuid


class TestCommerceUser:
    """Commerce User 모듈 통합 테스트"""

    def test_user_list(self, commerce_client):
        """사용자 목록 조회"""
        response = commerce_client.user.list({'page': 1, 'limit': 10})
        print(f"[Commerce] user.list = {response}")

        assert response is not None

    def test_user_list_with_keyword(self, commerce_client):
        """키워드로 사용자 검색"""
        response = commerce_client.user.list({
            'page': 1,
            'limit': 10,
            'keyword': 'test',
        })
        print(f"[Commerce] user.list (keyword) = {response}")

        assert response is not None

    def test_user_token(self, commerce_client):
        """사용자 토큰 발급"""
        response = commerce_client.user.token(user_id='test_user_001')
        print(f"[Commerce] user.token = {response}")

        assert response is not None

    def test_user_check_exist(self, commerce_client):
        """사용자 중복 체크"""
        response = commerce_client.user.check_exist(
            key='login_id',
            value='nonexistent_user_id',
        )
        print(f"[Commerce] user.check_exist = {response}")

        assert response is not None

    def test_user_detail_invalid(self, commerce_client):
        """존재하지 않는 사용자 상세 조회"""
        response = commerce_client.user.detail(user_id='nonexistent_user_id')
        print(f"[Commerce] user.detail (invalid) = {response}")

        assert response is not None

    def test_user_join_and_delete(self, commerce_client):
        """회원가입 후 삭제 (생성/삭제 순환 테스트)"""
        unique_id = f"test_{uuid.uuid4().hex[:8]}"
        user_data = {
            'login_id': unique_id,
            'login_pw': 'test1234!',
            'username': '테스트유저',
            'email': f'{unique_id}@test.bootpay.co.kr',
            'phone': '01000000000',
        }

        # 회원가입
        join_response = commerce_client.user.join(user_data)
        print(f"[Commerce] user.join = {join_response}")
        assert join_response is not None

        # 가입 성공 시 삭제까지 수행
        user_id = join_response.get('user_id')
        if user_id:
            delete_response = commerce_client.user.delete(user_id=user_id)
            print(f"[Commerce] user.delete = {delete_response}")

    def test_user_login_invalid(self, commerce_client):
        """잘못된 자격증명으로 로그인"""
        response = commerce_client.user.login(
            login_id='invalid_login',
            login_pw='invalid_pw',
        )
        print(f"[Commerce] user.login (invalid) = {response}")

        assert response is not None
