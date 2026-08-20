import uuid
from typing import TYPE_CHECKING, Optional, Dict
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

    구매자측 요청 생성 (pause/resume/purchase/termination/transfer) 은
    `commerce.order_subscription.request_ing.*` 모듈을 사용한다.

    ⚠️ 경로가 order-subscription-requests — 하이픈이다.
       order_subscriptions · order_subscription_bills 는 언더스코어라 복사해 고칠 때 가장 흔히 틀리는 지점.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[OrderSubscriptionRequestListParams] = None):
        """
        구독 변경요청 목록 조회 (user / supervisor 공용)
        GET /v1/order-subscription-requests
        project_id 를 주면 supervisor 모드(프로젝트 전체 검색), 없으면 본인 요청만 조회한다.
        page/limit 미지정시 각각 1 / 20 이 적용된다.
        :param params: 조회 파라미터
        :return: {'items': List[OrderSubscriptionRequest], 'total': int}
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)

        query_params = {}
        if params.get('project_id'):
            query_params['project_id'] = params['project_id']
        if params.get('order_subscription_id'):
            query_params['order_subscription_id'] = params['order_subscription_id']
        query_params['page'] = 1 if params.get('page') is None else params['page']
        query_params['limit'] = 20 if params.get('limit') is None else params['limit']
        if params.get('keyword'):
            query_params['keyword'] = params['keyword']
        if params.get('s_at'):
            query_params['s_at'] = params['s_at']
        if params.get('e_at'):
            query_params['e_at'] = params['e_at']
        if params.get('status') is not None:
            query_params['status'] = params['status']
        if params.get('request_type') is not None:
            query_params['request_type'] = params['request_type']
        if params.get('user_id'):
            query_params['user_id'] = params['user_id']
        if params.get('user_group_id'):
            query_params['user_group_id'] = params['user_group_id']

        return self._bootpay.get(
            f'order-subscription-requests?{urlencode(query_params)}',
            headers=self._request_headers(params.get('project_id'), idempotency_key)
        )

    def detail(
        self,
        order_subscription_request_history_id: str,
        project_id: Optional[str] = None,
        idempotency_key: Optional[str] = None
    ):
        """
        구독 변경요청 단건 조회 (user / supervisor 공용)
        GET /v1/order-subscription-requests/{id}
        :param order_subscription_request_history_id: 요청 이력 ID
        :param project_id: 프로젝트 ID (supervisor 모드에서 사용)
        :param idempotency_key: 미지정시 자동 생성
        :return: OrderSubscriptionRequest
        """
        query_params = {}
        if project_id:
            query_params['project_id'] = project_id

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(
            f'order-subscription-requests/{order_subscription_request_history_id}'
            f'{"?" + query if query else ""}',
            headers=self._request_headers(project_id, idempotency_key)
        )

    def update(self, params: OrderSubscriptionRequestUpdateParams):
        """
        구독 변경요청 승인/반려 (supervisor 전용)
        PUT /v1/order-subscription-requests/{id}
        ⚠️ 승인과 반려는 별도 액션이 아니다. 라우트는 index/show/update 셋뿐이고
           approval: 'approve' | 'reject' 파라미터로 갈린다.
           서버가 params[:action] 을 Rails 예약어로 쓰기 때문에 키 이름이 approval 이다.
        :param params: 승인/거절 파라미터 (order_subscription_request_history_id 필수)
        :return: OrderSubscriptionRequest
        """
        if not params.get('order_subscription_request_history_id'):
            raise ValueError('order_subscription_request_history_id is required')
        params = dict(params)
        history_id = params.pop('order_subscription_request_history_id')
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'order-subscription-requests/{history_id}',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def _request_headers(self, project_id: Optional[str] = None,
                         idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """조회 요청 헤더 — project_id 가 있으면 supervisor, 없으면 user scope 다."""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor' if project_id else 'user'
        }

    def _supervisor_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """승인/반려 요청 헤더 — 서버가 supervisor scope 를 요구한다."""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }
