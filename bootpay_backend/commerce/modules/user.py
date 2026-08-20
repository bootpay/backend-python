import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode, quote

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceUser,
    UserListParams,
    UserTokenResponse,
    UserLoginResponse,
    MallUserLoginParams,
    MallUserJoinParams,
    MallUserJoinCheckType,
    MallUserSessionResponse
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

    def user_login(self, params: MallUserLoginParams):
        """
        회원 로그인 (V1 API)
        POST /v1/users/login
        v1 에는 단수 user/* 라우트가 없다. 로그인은 v1/users/login#create 다.
        ⚠️ POST /v1/users/session 은 resource :session 이 만들어낸 라우트일 뿐 create 액션이 없다 — 그리로 보내면 안 된다.
        ⚠️ 서버(LoginService)는 login_id/password 만 읽는다. corporate_type 은 전달돼도 무시된다.
        :param params: 로그인 파라미터 (corporate_type 미지정시 0)
        :return: UserLoginResponse
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        corporate_type = params.pop('corporate_type', None)
        payload = self._compact(params)
        payload['corporate_type'] = 0 if corporate_type is None else corporate_type
        return self._bootpay.post(
            'users/login',
            payload,
            headers=self._mall_headers(idempotency_key=idempotency_key)
        )

    def user_session(self, user_jwt: Optional[str] = None, idempotency_key: Optional[str] = None):
        """
        회원 세션 조회 (V1 API)
        GET /v1/users/session
        :param user_jwt: 로그인시 발급받은 회원 JWT
        :param idempotency_key: 미지정시 자동 생성
        :return: MallUserSessionResponse
        """
        return self._bootpay.get(
            'users/session',
            headers=self._mall_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def user_logout(self, user_jwt: str, idempotency_key: Optional[str] = None):
        """
        회원 로그아웃 (V1 API)
        DELETE /v1/users/session
        :param user_jwt: 로그인시 발급받은 회원 JWT
        :param idempotency_key: 미지정시 자동 생성
        :return: None
        """
        return self._bootpay.delete(
            'users/session',
            headers=self._mall_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def user_join(self, params: MallUserJoinParams):
        """
        회원가입 (V1 API) — 일반 회원가입용
        POST /v1/users/join
        ⚠️ join(user) 과 같은 엔드포인트를 부른다. 중복이 아니라 용도가 다르다 —
           이쪽은 password/corporate_type/group 을 쓰는 일반 회원가입, 저쪽은 uid/login_email/login_pw 를 쓰는 외부 uid 연동 가입이다.
           서버가 파라미터 조합으로 분기하므로 둘 다 유지한다.
        :param params: 회원가입 파라미터 (corporate_type 미지정시 0, 나머지 None 값은 전송하지 않는다)
        :return: CommerceUser
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        corporate_type = params.pop('corporate_type', None)
        payload = self._compact(params)
        payload['corporate_type'] = 0 if corporate_type is None else corporate_type
        return self._bootpay.post(
            'users/join',
            payload,
            headers=self._mall_headers(idempotency_key=idempotency_key)
        )

    def user_join_check(self, type: MallUserJoinCheckType, pk: str, idempotency_key: Optional[str] = None):
        """
        회원가입 중복 확인 (V1 API) — key 를 인자로 받는 일반형
        GET /v1/users/join/{type}?pk={pk}
        ⚠️ uid_exist 등 전용형과 기능이 겹치지만 둘 다 유지한다.
           일반형은 서버에 새 key 가 생겨도 SDK 수정 없이 쓸 수 있다.
        :param type: email-exist, id-exist, phone-exist, uid-exist, group-business-number-exist
        :param pk: 중복 확인할 값
        :param idempotency_key: 미지정시 자동 생성
        :return: {'exists': bool}
        """
        return self._bootpay.get(
            f'users/join/{type}?pk={quote(pk, safe="")}',
            headers=self._mall_headers(idempotency_key=idempotency_key)
        )

    def uid_exist(self, uid: str, idempotency_key: Optional[str] = None):
        """
        외부 uid(ex_uid) 중복 검사
        GET /v1/users/join/uid-exist?pk={uid}
        email-exist / id-exist / phone-exist / group-business-number-exist 와 같은 전용형이다.
        :param uid: 중복 확인할 외부 uid
        :param idempotency_key: 미지정시 자동 생성
        :return: {'exists': bool}
        """
        headers = self._mall_headers(idempotency_key=idempotency_key)
        headers['BOOTPAY-ROLE'] = 'user'
        return self._bootpay.get(f'users/join/uid-exist?pk={quote(uid, safe="")}', headers=headers)

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

    def _compact(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """None 값을 제거한다."""
        return {k: v for k, v in payload.items() if v is not None}

    def _mall_headers(self, user_jwt: Optional[str] = None, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        V1 Mall API 요청 헤더
        Idempotency-Key 는 미지정시 매 호출마다 생성되고, Bootpay-User-JWT 는 값이 있을 때만 붙는다.
        """
        headers = {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4())
        }
        if user_jwt:
            headers['Bootpay-User-JWT'] = user_jwt
        return headers
