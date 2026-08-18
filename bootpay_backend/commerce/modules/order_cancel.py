from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    OrderCancelListParams,
    OrderCancelParams,
    OrderCancelActionParams,
    CommerceOrderCancelRequestHistory
)


class OrderCancelModule:
    """주문 취소 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    @staticmethod
    def _cancellation_id(params: OrderCancelActionParams) -> str:
        """
        취소요청 ID 추출
        서버(v1/order/cancel_controller)는 approve/reject/withdraw 모두 :id를
        order_cancellation_request_id로 동일하게 취급한다.
        기존 키(order_cancel_request_history_id)도 하위호환으로 계속 지원한다.
        """
        cancellation_id = (
            params.get('order_cancellation_request_id')
            or params.get('order_cancel_request_history_id')
        )
        if not cancellation_id:
            raise ValueError('order_cancellation_request_id is required')
        return cancellation_id

    def list(self, params: Optional[OrderCancelListParams] = None):
        """
        취소 요청 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceOrderCancelRequestHistory], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('order_id'):
                query_params['order_id'] = params['order_id']
            if params.get('order_number'):
                query_params['order_number'] = params['order_number']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'order/cancel{"?" + query if query else ""}')

    def request(self, params: OrderCancelParams):
        """
        취소 요청
        :param params: 취소 요청 파라미터
        :return: CommerceOrderCancelRequestHistory
        """
        return self._bootpay.post('order/cancel', params)

    def withdraw(self, order_cancel_request_history_id: str):
        """
        (구매자) 취소 요청 철회 (PUT /v1/order/cancel/:id/withdraw)
        :param order_cancel_request_history_id: 취소 요청 ID (order_cancellation_request_id)
        :return: None
        """
        return self._bootpay.put(f'order/cancel/{order_cancel_request_history_id}/withdraw', {})

    def approve(self, params: OrderCancelActionParams):
        """
        (관리자) 취소 승인 (PUT /v1/order/cancel/:id/approve)
        :param params: 취소 승인 파라미터
                       (order_cancellation_request_id 또는 order_cancel_request_history_id)
        :return: CommerceOrderCancelRequestHistory
        """
        return self._bootpay.put(
            f'order/cancel/{self._cancellation_id(params)}/approve',
            params
        )

    def reject(self, params: OrderCancelActionParams):
        """
        (관리자) 취소 거절 (PUT /v1/order/cancel/:id/reject)
        :param params: 취소 거절 파라미터
                       (order_cancellation_request_id 또는 order_cancel_request_history_id)
        :return: CommerceOrderCancelRequestHistory
        """
        return self._bootpay.put(
            f'order/cancel/{self._cancellation_id(params)}/reject',
            params
        )
