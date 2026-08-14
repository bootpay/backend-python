import uuid
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceUser,
    UserListParams,
    UserTokenResponse,
    UserLoginResponse
)


class UserModule:
    """사용자 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def token(self, user_id: str):
        """
        사용자 토큰 발급
        :param user_id: 사용자 ID
        :return: UserTokenResponse
        """
        return self._bootpay.post('users/login/token', {'user_id': user_id})

    def join(self, user: CommerceUser):
        """
        회원가입
        :param user: 사용자 정보
        :return: CommerceUser
        """
        return self._bootpay.post('users/join', user)

    def check_exist(self, key: str, value: str):
        """
        중복 체크
        :param key: 체크할 필드 (login_id, phone, email 등)
        :param value: 체크할 값
        :return: {'exists': bool}
        """
        from urllib.parse import quote
        encoded_value = quote(value, safe='')
        return self._bootpay.get(f'users/join/{key}?pk={encoded_value}')

    def authentication_data(self, stand_id: str):
        """
        본인인증 데이터 조회
        :param stand_id: 인증 ID
        :return: 인증 데이터
        """
        return self._bootpay.get(f'users/authenticate/{stand_id}')

    def login(self, login_id: str, login_pw: str):
        """
        로그인
        :param login_id: 로그인 ID
        :param login_pw: 비밀번호
        :return: UserLoginResponse
        """
        return self._bootpay.post('users/login', {
            'login_id': login_id,
            'login_pw': login_pw
        })

    def user_login(self, login_id: str, login_pw: str):
        """회원 로그인 (Mall API alias)"""
        return self.login(login_id, login_pw)

    def user_join(self, user: CommerceUser):
        """회원가입 (Mall API alias)"""
        return self.join(user)

    def user_join_check(self, check_type: str, pk: str):
        """회원가입 중복 확인 (Mall API alias)"""
        return self.check_exist(check_type, pk)

    def _mall_headers(self, user_jwt: Optional[str] = None, idempotency_key: Optional[str] = None):
        """Mall API 전용 헤더 생성"""
        headers = {'Idempotency-Key': idempotency_key or str(uuid.uuid4())}
        if user_jwt:
            headers['Bootpay-User-JWT'] = user_jwt
        return headers

    def user_session(self, user_jwt: Optional[str] = None, idempotency_key: Optional[str] = None):
        """
        회원 세션 조회 (V1 Mall API)
        :param user_jwt: 회원 JWT
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 회원 세션 정보
        """
        return self._bootpay.get('user/session', headers=self._mall_headers(user_jwt, idempotency_key))

    def user_logout(self, user_jwt: str, idempotency_key: Optional[str] = None):
        """
        회원 로그아웃 (V1 Mall API)
        :param user_jwt: 회원 JWT
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 로그아웃 결과
        """
        return self._bootpay.delete('user/session', headers=self._mall_headers(user_jwt, idempotency_key))

    def list(self, params: Optional[UserListParams] = None):
        """
        사용자 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceUser], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']
            if params.get('member_type') is not None:
                query_params['member_type'] = params['member_type']
            if params.get('type'):
                query_params['type'] = params['type']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'users{"?" + query if query else ""}')

    def detail(self, user_id: str):
        """
        사용자 상세 조회
        :param user_id: 사용자 ID
        :return: CommerceUser
        """
        return self._bootpay.get(f'users/{user_id}')

    def update(self, user: CommerceUser):
        """
        사용자 정보 수정
        :param user: 사용자 정보
        :return: CommerceUser
        """
        if not user.get('user_id'):
            raise ValueError('user_id is required')
        return self._bootpay.put(f'users/{user["user_id"]}', user)

    def delete(self, user_id: str):
        """
        사용자 삭제 (회원탈퇴)
        :param user_id: 사용자 ID
        :return: None
        """
        return self._bootpay.delete(f'users/{user_id}')
