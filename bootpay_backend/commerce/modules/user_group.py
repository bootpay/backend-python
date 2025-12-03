from typing import TYPE_CHECKING, Optional
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

    def user_create(self, user_group_id: str, user_id: str):
        """
        그룹에 사용자 추가
        :param user_group_id: 그룹 ID
        :param user_id: 사용자 ID
        :return: None
        """
        return self._bootpay.post(f'user-groups/{user_group_id}/add_user', {'user_id': user_id})

    def user_delete(self, user_group_id: str, user_id: str):
        """
        그룹에서 사용자 제거
        :param user_group_id: 그룹 ID
        :param user_id: 사용자 ID
        :return: None
        """
        return self._bootpay.delete(f'user-groups/{user_group_id}/remove_user?user_id={user_id}')

    def limit(self, params: UserGroupLimitParams):
        """
        그룹 제한 설정
        :param params: 제한 설정 파라미터
        :return: CommerceUserGroup
        """
        if not params.get('user_group_id'):
            raise ValueError('user_group_id is required')
        return self._bootpay.put(f'user-groups/{params["user_group_id"]}/limit', params)

    def aggregate_transaction(self, params: UserGroupAggregateTransactionParams):
        """
        그룹 거래 집계 조회
        :param params: 집계 파라미터
        :return: 집계 결과
        """
        if not params.get('user_group_id'):
            raise ValueError('user_group_id is required')
        return self._bootpay.put(f'user-groups/{params["user_group_id"]}/aggregate-transaction', params)
