import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceUserGroup,
    UserGroupListParams,
    UserGroupLimitParams,
    UserGroupAggregateTransactionParams
)


class UserGroupModule:
    """사용자 그룹 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def create(self, user_group: CommerceUserGroup):
        """
        사용자 그룹 생성
        :param user_group: 그룹 정보
        :return: CommerceUserGroup
        """
        return self._bootpay.post('user-groups', user_group)

    def list(self, params: Optional[UserGroupListParams] = None):
        """
        사용자 그룹 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceUserGroup], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']
            if params.get('corporate_type') is not None:
                query_params['corporate_type'] = params['corporate_type']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'user-groups{"?" + query if query else ""}')

    def detail(self, user_group_id: str):
        """
        사용자 그룹 상세 조회
        :param user_group_id: 그룹 ID
        :return: CommerceUserGroup
        """
        return self._bootpay.get(f'user-groups/{user_group_id}')

    def update(self, user_group: CommerceUserGroup):
        """
        사용자 그룹 수정
        :param user_group: 그룹 정보
        :return: CommerceUserGroup
        """
        if not user_group.get('user_group_id'):
            raise ValueError('user_group_id is required')
        return self._bootpay.put(f'user-groups/{user_group["user_group_id"]}', user_group)

    def user_create(self, user_group_id: str, user_id: str, idempotency_key: Optional[str] = None):
        """
        그룹에 사용자 추가
        POST /v1/user-groups/{user_group_id}/user
        ⚠️ 서버가 manager scope 를 요구한다 (scope_invalid!).
        :param user_group_id: 그룹 ID
        :param user_id: 사용자 ID
        :param idempotency_key: 미지정시 자동 생성
        :return: None
        """
        return self._bootpay.post(
            f'user-groups/{user_group_id}/user',
            {'user_id': user_id},
            headers=self._manager_headers(idempotency_key)
        )

    def user_delete(self, user_group_id: str, user_id: str, idempotency_key: Optional[str] = None):
        """
        그룹에서 사용자 제거
        DELETE /v1/user-groups/{user_group_id}/user/{user_id}
        ⚠️ 서버가 manager scope 를 요구한다 (scope_invalid!).
        :param user_group_id: 그룹 ID
        :param user_id: 사용자 ID
        :param idempotency_key: 미지정시 자동 생성
        :return: None
        """
        return self._bootpay.delete(
            f'user-groups/{user_group_id}/user/{user_id}',
            headers=self._manager_headers(idempotency_key)
        )

    def limit(self, params: UserGroupLimitParams):
        """
        그룹 구매한도 설정
        PUT /v1/user-groups/{user_group_id}/limit
        ⚠️ update 로는 한도가 절대 반영되지 않는다 — 서버 user_groups_controller#update 가
           use_limit / limit_message / limit_month_purchase / limit_week_purchase 를 명시적으로 제거하기 때문이다.
           한도는 이 전용 라우트로만 바뀐다. 서버 scope: manager:limit
        :param params: 제한 설정 파라미터
        :return: CommerceUserGroup
        """
        if not params.get('user_group_id'):
            raise ValueError('user_group_id is required')
        params = dict(params)
        user_group_id = params.pop('user_group_id')
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'user-groups/{user_group_id}/limit',
            payload,
            headers=self._manager_headers(idempotency_key)
        )

    def aggregate_transaction(self, params: UserGroupAggregateTransactionParams):
        """
        그룹 구독 합산청구(정산주기) 설정 변경
        PUT /v1/user-groups/{user_group_id}/aggregate-transaction
        update 에도 같은 이름의 인자가 있지만 서버는 이 전용 라우트에서만 처리한다.
        :param params: 집계 파라미터
        :return: 집계 결과
        """
        if not params.get('user_group_id'):
            raise ValueError('user_group_id is required')
        params = dict(params)
        user_group_id = params.pop('user_group_id')
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'user-groups/{user_group_id}/aggregate-transaction',
            payload,
            headers=self._manager_headers(idempotency_key)
        )

    def _manager_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        그룹 멤버십/한도/합산청구 요청 헤더 — 서버가 manager scope 를 요구한다.
        Idempotency-Key 는 미지정시 매 호출마다 생성된다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'manager'
        }
