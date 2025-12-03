from typing import TYPE_CHECKING, Optional, List
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceOrder,
    OrderListParams
)


class OrderModule:
    """주문 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[OrderListParams] = None):
        """
        주문 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceOrder], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']
            if params.get('user_id'):
                query_params['user_id'] = params['user_id']
            if params.get('user_group_id'):
                query_params['user_group_id'] = params['user_group_id']
            if params.get('cs_type'):
                query_params['cs_type'] = params['cs_type']
            if params.get('css_at'):
                query_params['css_at'] = params['css_at']
            if params.get('cse_at'):
                query_params['cse_at'] = params['cse_at']
            if params.get('subscription_billing_type') is not None:
                query_params['subscription_billing_type'] = params['subscription_billing_type']
            if params.get('status') and len(params['status']) > 0:
                query_params['status'] = ','.join(map(str, params['status']))
            if params.get('payment_status') and len(params['payment_status']) > 0:
                query_params['payment_status'] = ','.join(map(str, params['payment_status']))
            if params.get('order_subscription_ids') and len(params['order_subscription_ids']) > 0:
                query_params['order_subscription_ids'] = ','.join(params['order_subscription_ids'])

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'orders{"?" + query if query else ""}')

    def detail(self, order_id: str):
        """
        주문 상세 조회
        :param order_id: 주문 ID
        :return: CommerceOrder
        """
        return self._bootpay.get(f'orders/{order_id}')

    def month(self, user_group_id: str, search_date: str):
        """
        월별 주문 조회
        :param user_group_id: 사용자 그룹 ID
        :param search_date: 검색 날짜 (YYYY-MM 형식)
        :return: 월별 주문 데이터
        """
        query_params = {
            'user_group_id': user_group_id,
            'search_date': search_date
        }
        return self._bootpay.get(f'orders/month?{urlencode(query_params)}')
