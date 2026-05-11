from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    OrderSubscriptionRequest,
    OrderSubscriptionRequestListParams,
    OrderSubscriptionRequestUpdateParams
)


class OrderSubscriptionRequestModule:
    """
    V1 OrderSubscription Request 조회/승인 모듈

    본인 모드 (user role): project_id 없이 호출 → 본인 요청 목록/단건
    슈퍼바이저 모드 (supervisor role): project_id 포함 → 프로젝트 전체 + update (승인/거절)

    구매자측 요청 생성 (pause/resume/termination 등) 은
    `commerce.order_subscription.request_ing.*` 모듈을 사용한다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[OrderSubscriptionRequestListParams] = None):
        """
        요청 목록 조회 (user / supervisor 공용)
        :param params: 조회 파라미터
        :return: {'items': List[OrderSubscriptionRequest], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('project_id'):
                query_params['project_id'] = params['project_id']
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('request_type') is not None:
                query_params['request_type'] = params['request_type']
            if params.get('status') is not None:
                query_params['status'] = params['status']
            if params.get('s_at'):
                query_params['s_at'] = params['s_at']
            if params.get('e_at'):
                query_params['e_at'] = params['e_at']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(
            f'order-subscription-requests{"?" + query if query else ""}'
        )

    def detail(
        self,
        order_subscription_request_history_id: str,
        project_id: Optional[str] = None
    ):
        """
        요청 단건 조회 (user / supervisor 공용)
        :param order_subscription_request_history_id: 요청 이력 ID
        :param project_id: 프로젝트 ID (supervisor 모드에서 사용)
        :return: OrderSubscriptionRequest
        """
        query_params = {}
        if project_id:
            query_params['project_id'] = project_id

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(
            f'order-subscription-requests/{order_subscription_request_history_id}'
            f'{"?" + query if query else ""}'
        )

    def update(self, params: OrderSubscriptionRequestUpdateParams):
        """
        요청 승인/거절 (supervisor 전용)
        :param params: 승인/거절 파라미터 (order_subscription_request_history_id 필수)
        :return: OrderSubscriptionRequest
        """
        if not params.get('order_subscription_request_history_id'):
            raise ValueError('order_subscription_request_history_id is required')
        history_id = params['order_subscription_request_history_id']
        rest = {k: v for k, v in params.items() if k != 'order_subscription_request_history_id'}
        return self._bootpay.put(
            f'order-subscription-requests/{history_id}',
            rest
        )
