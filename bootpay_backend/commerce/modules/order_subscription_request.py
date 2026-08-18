import uuid
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    OrderSubscriptionRequestListParams,
    OrderSubscriptionRequestUpdateParams
)


class OrderSubscriptionRequestModule:
    """
    정기구독 변경요청 모듈 (order-subscription-requests)

    경로가 하이픈(order-subscription-requests)이다.
    order_subscriptions / order_subscription_bills 는 언더스코어이므로 혼동에 주의한다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def _request_headers(self, role: str, idempotency_key: Optional[str] = None):
        """요청 전용 헤더 생성"""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': role
        }

    def list(self, params: Optional[OrderSubscriptionRequestListParams] = None,
             idempotency_key: Optional[str] = None):
        """
        정기구독 변경요청 목록 조회 (GET /v1/order-subscription-requests)
        project_id를 지정하면 supervisor 모드(프로젝트 전체 검색), 없으면 본인 요청만 조회된다.
        :param params: 조회 파라미터 (project_id, order_subscription_id, page, limit, keyword,
                       s_at, e_at, status, request_type, user_id, user_group_id)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: {'list': List[dict], 'count': int}
        """
        query_params = {'page': 1, 'limit': 20}
        if params:
            query_params.update({key: value for key, value in params.items() if value is not None})

        role = 'supervisor' if query_params.get('project_id') else 'user'
        return self._bootpay.get(
            'order-subscription-requests',
            params=query_params,
            headers=self._request_headers(role, idempotency_key)
        )

    def detail(self, request_history_id: str, project_id: Optional[str] = None,
               idempotency_key: Optional[str] = None):
        """
        정기구독 변경요청 상세 조회 (GET /v1/order-subscription-requests/:id)
        :param request_history_id: 변경요청 이력 ID
        :param project_id: 프로젝트 ID (지정시 supervisor 모드)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 변경요청 상세
        """
        role = 'supervisor' if project_id else 'user'
        return self._bootpay.get(
            f'order-subscription-requests/{request_history_id}',
            params={'project_id': project_id} if project_id else None,
            headers=self._request_headers(role, idempotency_key)
        )

    def update(self, params: OrderSubscriptionRequestUpdateParams,
               idempotency_key: Optional[str] = None):
        """
        정기구독 변경요청 승인/반려 (PUT /v1/order-subscription-requests/:id)

        승인과 반려는 별도 엔드포인트가 아니라 approval 값('approve' | 'reject')으로 구분한다.
        (서버가 params[:action]을 예약어로 사용하기 때문에 키 이름이 approval 이다)
        :param params: 파라미터 (request_history_id, approval, reason, price, tax_free_price,
                       termination_fee, last_bill_refund_price, final_fee, service_end_at)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 변경요청 처리 결과
        """
        if not params.get('request_history_id'):
            raise ValueError('request_history_id is required')
        if not params.get('approval'):
            raise ValueError('approval is required')

        payload = {
            key: value for key, value in params.items()
            if key != 'request_history_id' and value is not None
        }
        return self._bootpay.put(
            f'order-subscription-requests/{params["request_history_id"]}',
            payload,
            headers=self._request_headers('supervisor', idempotency_key)
        )
