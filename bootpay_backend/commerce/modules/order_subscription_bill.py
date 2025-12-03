from typing import TYPE_CHECKING, Optional, List
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceOrderSubscriptionBill,
    OrderSubscriptionBillListParams
)


class OrderSubscriptionBillModule:
    """정기구독 청구 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[OrderSubscriptionBillListParams] = None):
        """
        정기구독 청구 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceOrderSubscriptionBill], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']
            if params.get('order_subscription_id'):
                query_params['order_subscription_id'] = params['order_subscription_id']
            if params.get('status') and len(params['status']) > 0:
                query_params['status'] = ','.join(map(str, params['status']))

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'order_subscription_bills{"?" + query if query else ""}')

    def detail(self, order_subscription_bill_id: str):
        """
        정기구독 청구 상세 조회
        :param order_subscription_bill_id: 청구 ID
        :return: CommerceOrderSubscriptionBill
        """
        return self._bootpay.get(f'order_subscription_bills/{order_subscription_bill_id}')

    def update(self, order_subscription_bill: CommerceOrderSubscriptionBill):
        """
        정기구독 청구 수정
        :param order_subscription_bill: 청구 정보
        :return: CommerceOrderSubscriptionBill
        """
        if not order_subscription_bill.get('order_subscription_bill_id'):
            raise ValueError('order_subscription_bill_id is required')
        return self._bootpay.put(
            f'order_subscription_bills/{order_subscription_bill["order_subscription_bill_id"]}',
            order_subscription_bill
        )
