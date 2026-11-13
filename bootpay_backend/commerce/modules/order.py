import uuid
from typing import TYPE_CHECKING, Optional, List, Dict
from urllib.parse import urlencode, quote

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceOrder,
    OrderListParams,
    OrderPurchaseUpdateItem
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
            if params.get('search_date_from'):
                query_params['search_date_from'] = params['search_date_from']
            if params.get('search_date_to'):
                query_params['search_date_to'] = params['search_date_to']
            # css_at / cse_at 는 서버 별칭으로 계속 지원 (정식 키는 search_date_from / search_date_to)
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
                query_params['order_subscription_ids'] = ','.join(map(str, params['order_subscription_ids']))

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

    def purchases(self, order_number: str, idempotency_key: Optional[str] = None):
        """
        발송 정보 조회 — 발주(배송) 단위 운송장·택배사·배송추적 상태·이력
        GET /v1/orders/{order_number}/purchases
        주문번호(order_number) 기준이다(order_id 아님). BOOTPAY-ROLE 은 user 로 고정한다.
        :param order_number: 주문번호
        :param idempotency_key: 미지정시 자동 생성
        """
        return self._bootpay.get(
            f'orders/{quote(str(order_number), safe="")}/purchases',
            headers=self._user_headers(idempotency_key)
        )

    def update_purchases(self, order_number: str, purchases: List[OrderPurchaseUpdateItem],
                         idempotency_key: Optional[str] = None):
        """
        발송처리 — 발주(배송) 단위 상태·운송장 갱신
        PUT /v1/orders/{order_number}/purchases
        경로 주문에 딸리지 않은 order_purchase_number 가 섞이면 요청 전체가 ORDER_PURCHASE_NOT_FOUND 로 거절된다. 한 번에 최대 50건.
        :param order_number: 주문번호 (경로로만 보낸다)
        :param purchases: 발주 갱신 목록 (order_purchase_number, status 필수)
        :param idempotency_key: 미지정시 자동 생성 (헤더로만 보낸다)
        """
        return self._bootpay.put(
            f'orders/{quote(str(order_number), safe="")}/purchases',
            {'purchases': purchases},
            headers=self._user_headers(idempotency_key)
        )

    def _user_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """구매자 scope 요청 헤더"""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'user'
        }
