import uuid
from typing import TYPE_CHECKING, Optional, Union, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    OrderCancelListParams,
    OrderCancelParams,
    OrderCancelActionParams,
    OrderCancelWithdrawParams,
    CommerceOrderCancelRequestHistory
)


class OrderCancelModule:
    """주문 취소 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[OrderCancelListParams] = None):
        """
        주문 취소 요청 내역 조회
        GET /v1/order/cancel
        order_number 또는 order_id 로 필터한다. 둘 다 없으면 전체.
        approve / reject / withdraw 에 넘길 order_cancellation_request_id 를 여기서 얻는다.
        :param params: 조회 파라미터
        :return: {'items': List[CommerceOrderCancelRequestHistory], 'total': int}
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)

        query_params = {}
        if params.get('order_number'):
            query_params['order_number'] = params['order_number']
        if params.get('order_id'):
            query_params['order_id'] = params['order_id']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(
            f'order/cancel{"?" + query if query else ""}',
            headers=self._user_headers(idempotency_key)
        )

    def request(self, params: OrderCancelParams):
        """
        취소 요청
        :param params: 취소 요청 파라미터
        :return: CommerceOrderCancelRequestHistory
        """
        return self._bootpay.post('order/cancel', params)

    def withdraw(self, order_cancellation_request_id: Union[str, OrderCancelWithdrawParams, None] = None,
                 idempotency_key: Optional[str] = None,
                 order_cancel_request_history_id: Optional[str] = None):
        """
        (구매자) 주문 취소 요청 철회
        PUT /v1/order/cancel/{order_cancellation_request_id}/withdraw
        ⚠️ DELETE /v1/order/cancel/{id} 와는 다른 라우트다. 서버에 둘 다 있지만 매뉴얼이 문서화한 쪽은 withdraw 다.
        정식 인자명은 order_cancellation_request_id 이며,
        구 이름 order_cancel_request_history_id (positional/keyword 모두) 도 계속 동작한다.
        :param order_cancellation_request_id: 취소 요청 이력 ID (문자열) 또는 파라미터 dict
        :param idempotency_key: 미지정시 자동 생성
        :return: None
        """
        params = order_cancellation_request_id
        if isinstance(params, dict):
            cancellation_id = self._cancellation_id(params)
            idempotency_key = idempotency_key or params.get('idempotency_key')
        else:
            cancellation_id = params or order_cancel_request_history_id
        if not cancellation_id:
            raise ValueError('order_cancellation_request_id is required')
        return self._bootpay.put(
            f'order/cancel/{cancellation_id}/withdraw',
            {},
            headers=self._user_headers(idempotency_key)
        )

    def approve(self, params: OrderCancelActionParams):
        """
        (관리자) 취소 요청 승인
        PUT /v1/order/cancel/{order_cancellation_request_id}/approve
        :param params: 취소 승인 파라미터
        :return: CommerceOrderCancelRequestHistory
        """
        cancellation_id = self._cancellation_id(params)
        if not cancellation_id:
            raise ValueError('order_cancellation_request_id is required')
        return self._bootpay.put(
            f'order/cancel/{cancellation_id}/approve',
            self._action_payload(params),
            headers=self._supervisor_headers(params.get('idempotency_key'))
        )

    def reject(self, params: OrderCancelActionParams):
        """
        (관리자) 취소 요청 반려
        PUT /v1/order/cancel/{order_cancellation_request_id}/reject
        :param params: 취소 거절 파라미터
        :return: CommerceOrderCancelRequestHistory
        """
        cancellation_id = self._cancellation_id(params)
        if not cancellation_id:
            raise ValueError('order_cancellation_request_id is required')
        return self._bootpay.put(
            f'order/cancel/{cancellation_id}/reject',
            self._action_payload(params),
            headers=self._supervisor_headers(params.get('idempotency_key'))
        )

    def _cancellation_id(self, params: Dict[str, Any]) -> Optional[str]:
        """
        취소 요청 이력 ID 를 뽑는다.
        서버는 approve / reject / withdraw 셋 다 params[:id] 를 order_cancellation_request_id 로 동일하게 취급한다.
        정식 이름은 order_cancellation_request_id 이며, 구 이름 order_cancel_request_history_id 도 계속 받는다.
        """
        return params.get('order_cancellation_request_id') or params.get('order_cancel_request_history_id')

    def _action_payload(self, params: OrderCancelActionParams) -> Dict[str, Any]:
        """승인/반려 payload — 서버가 읽는 값은 message 다."""
        excluded = ('order_cancellation_request_id', 'order_cancel_request_history_id', 'idempotency_key')
        return {k: v for k, v in params.items() if k not in excluded and v is not None}

    def _user_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """구매자 scope 요청 헤더"""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'user'
        }

    def _supervisor_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """관리자(승인/반려) scope 요청 헤더"""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }
