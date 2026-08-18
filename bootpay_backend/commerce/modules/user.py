import uuid
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceUser,
    UserListParams,
    UserTokenResponse,
    UserLoginResponse,
    MallUserJoinParams
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

    def _mall_headers(self, user_jwt: Optional[str] = None, idempotency_key: Optional[str] = None):
        """Mall API 전용 헤더 생성"""
        headers = {'Idempotency-Key': idempotency_key or str(uuid.uuid4())}
        if user_jwt:
            headers['Bootpay-User-JWT'] = user_jwt
        return headers

    def user_login(self, login_id: str, password: str, corporate_type: int = 0,
                   idempotency_key: Optional[str] = None):
        """
        회원 로그인 (V1 API)
        v1에는 단수 user/* 라우트가 없다. 로그인은 POST /v1/users/login 이다.
        (POST /v1/users/session 은 라우트만 존재할 뿐 create 액션이 없으므로 사용하지 않는다)
        서버는 login_id/password만 읽으며 corporate_type은 전달되어도 무시된다.
        :param login_id: 로그인 ID
        :param password: 비밀번호
        :param corporate_type: 회원 유형 (0: 개인, 1: 사업자)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 로그인 결과
        """
        payload = {
            'login_id': login_id,
            'password': password,
            'corporate_type': corporate_type
        }
        return self._bootpay.post(
            'users/login',
            {key: value for key, value in payload.items() if value is not None},
            headers=self._mall_headers(idempotency_key=idempotency_key)
        )

    def user_join(self, user: MallUserJoinParams, idempotency_key: Optional[str] = None):
        """
        회원가입 (V1 API) - 일반 회원가입용 (POST /v1/users/join)
        join()과 같은 엔드포인트를 호출하지만 용도가 다르다.
        이쪽은 password/corporate_type/group을 쓰는 일반 회원가입이며,
        서버가 파라미터 조합으로 분기하므로 두 메서드를 모두 유지한다.
        :param user: 회원 정보 (login_id, password, name, email, phone, nickname, gender, birth,
                     corporate_type, group)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 회원가입 결과
        """
        payload = {key: value for key, value in (user or {}).items() if value is not None}
        return self._bootpay.post(
            'users/join',
            payload,
            headers=self._mall_headers(idempotency_key=idempotency_key)
        )

    def user_join_check(self, check_type: str, pk: str, idempotency_key: Optional[str] = None):
        """
        회원가입 중복 확인 (V1 API) - key를 인자로 받는 일반형 (GET /v1/users/join/:id)
        서버에 새 key가 추가되어도 SDK 수정 없이 사용할 수 있다.
        :param check_type: 중복 확인 유형
                           (email-exist, id-exist, phone-exist, uid-exist,
                            group-business-number-exist)
        :param pk: 중복 확인할 값
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: {'exists': bool}
        """
        return self._bootpay.get(
            f'users/join/{check_type}',
            params={'pk': pk},
            headers=self._mall_headers(idempotency_key=idempotency_key)
        )

    def user_session(self, user_jwt: Optional[str] = None, idempotency_key: Optional[str] = None):
        """
        회원 세션 조회 (V1 API - GET /v1/users/session)
        :param user_jwt: 회원 JWT
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 회원 세션 정보
        """
        return self._bootpay.get('users/session', headers=self._mall_headers(user_jwt, idempotency_key))

    def user_logout(self, user_jwt: str, idempotency_key: Optional[str] = None):
        """
        회원 로그아웃 (V1 API - DELETE /v1/users/session)
        :param user_jwt: 회원 JWT
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 로그아웃 결과
        """
        return self._bootpay.delete('users/session', headers=self._mall_headers(user_jwt, idempotency_key))

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
