from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceOrderSubscription,
    OrderSubscriptionListParams,
    OrderSubscriptionUpdateParams,
    OrderSubscriptionPauseParams,
    OrderSubscriptionResumeParams,
    OrderSubscriptionTerminationParams,
    CalcTerminateFeeResponse
)


class OrderSubscriptionRequestIngModule:
    """정기구독 진행 중 요청 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def pause(self, params: OrderSubscriptionPauseParams):
        """
        정기구독 일시정지
        :param params: 일시정지 파라미터
        :return: CommerceOrderSubscription
        """
        return self._bootpay.post('order_subscriptions/requests/ing/pause', params)

    def resume(self, params: OrderSubscriptionResumeParams):
        """
        정기구독 재개
        :param params: 재개 파라미터
        :return: CommerceOrderSubscription
        """
        return self._bootpay.put('order_subscriptions/requests/ing/resume', params)

    def calculate_termination_fee(
        self,
        order_subscription_id: Optional[str] = None,
        order_number: Optional[str] = None
    ):
        """
        해지 수수료 계산
        :param order_subscription_id: 정기구독 ID (선택)
        :param order_number: 주문번호 (선택)
        :return: CalcTerminateFeeResponse
        """
        if not order_subscription_id and not order_number:
            raise ValueError('order_subscription_id or order_number is required')

        query_params = {}
        if order_subscription_id:
            query_params['order_subscription_id'] = order_subscription_id
        elif order_number:
            query_params['order_number'] = order_number

        return self._bootpay.get(
            f'order_subscriptions/requests/ing/calculate_termination_fee?{urlencode(query_params)}'
        )

    def calculate_termination_fee_by_order_number(self, order_number: str):
        """
        주문번호로 해지 수수료 계산
        :param order_number: 주문번호
        :return: CalcTerminateFeeResponse
        """
        return self.calculate_termination_fee(order_number=order_number)

    def termination(self, params: OrderSubscriptionTerminationParams):
        """
        정기구독 해지
        :param params: 해지 파라미터
        :return: CommerceOrderSubscription
        """
        return self._bootpay.post('order_subscriptions/requests/ing/termination', params)


class OrderSubscriptionModule:
    """정기구독 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay
        self.request_ing = OrderSubscriptionRequestIngModule(bootpay)

    def list(self, params: Optional[OrderSubscriptionListParams] = None):
        """
        정기구독 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceOrderSubscription], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']
            if params.get('s_at'):
                query_params['s_at'] = params['s_at']
            if params.get('e_at'):
                query_params['e_at'] = params['e_at']
            if params.get('request_type'):
                query_params['request_type'] = params['request_type']
            if params.get('user_group_id'):
                query_params['user_group_id'] = params['user_group_id']
            if params.get('user_id'):
                query_params['user_id'] = params['user_id']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'order_subscriptions{"?" + query if query else ""}')

    def detail(self, order_subscription_id: str):
        """
        정기구독 상세 조회
        :param order_subscription_id: 정기구독 ID
        :return: CommerceOrderSubscription
        """
        return self._bootpay.get(f'order_subscriptions/{order_subscription_id}')

    def update(self, params: OrderSubscriptionUpdateParams):
        """
        정기구독 수정
        :param params: 수정 파라미터
        :return: CommerceOrderSubscription
        """
        if not params.get('order_subscription_id'):
            raise ValueError('order_subscription_id is required')
        return self._bootpay.put(f'order_subscriptions/{params["order_subscription_id"]}', params)
