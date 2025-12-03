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
        취소 요청 철회
        :param order_cancel_request_history_id: 취소 요청 이력 ID
        :return: None
        """
        return self._bootpay.put(f'order/cancel/{order_cancel_request_history_id}/withdraw', {})

    def approve(self, params: OrderCancelActionParams):
        """
        취소 승인
        :param params: 취소 승인 파라미터
        :return: CommerceOrderCancelRequestHistory
        """
        if not params.get('order_cancel_request_history_id'):
            raise ValueError('order_cancel_request_history_id is required')
        return self._bootpay.put(
            f'order/cancel/{params["order_cancel_request_history_id"]}/approve',
            params
        )

    def reject(self, params: OrderCancelActionParams):
        """
        취소 거절
        :param params: 취소 거절 파라미터
        :return: CommerceOrderCancelRequestHistory
        """
        if not params.get('order_cancel_request_history_id'):
            raise ValueError('order_cancel_request_history_id is required')
        return self._bootpay.put(
            f'order/cancel/{params["order_cancel_request_history_id"]}/reject',
            params
        )
