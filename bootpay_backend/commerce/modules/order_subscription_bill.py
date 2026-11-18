import uuid
from typing import TYPE_CHECKING, Optional, List, Dict
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
        정기구독 빌(회차) 목록 조회
        GET /v1/order_subscription_bills
        ⚠️ 경로가 order_subscription_bills — 언더스코어다 (하이픈 아님).
        page/limit 미지정시 각각 1 / 20 이 적용된다.
        :param params: 조회 파라미터
        :return: {'items': List[CommerceOrderSubscriptionBill], 'total': int}
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)

        query_params = {}
        if params.get('order_subscription_id'):
            query_params['order_subscription_id'] = params['order_subscription_id']
        query_params['page'] = 1 if params.get('page') is None else params['page']
        query_params['limit'] = 20 if params.get('limit') is None else params['limit']
        if params.get('keyword'):
            query_params['keyword'] = params['keyword']
        if params.get('status') and len(params['status']) > 0:
            query_params['status'] = ','.join(map(str, params['status']))

        return self._bootpay.get(
            f'order_subscription_bills?{urlencode(query_params)}',
            headers=self._user_headers(idempotency_key)
        )

    def detail(self, order_subscription_bill_id: str):
        """
        정기구독 청구 상세 조회
        :param order_subscription_bill_id: 청구 ID
        :return: CommerceOrderSubscriptionBill
        """
        return self._bootpay.get(
            f'order_subscription_bills/{order_subscription_bill_id}',
            # 상세는 원래 헤더가 없었다 — role 만 고정하고 Idempotency-Key 는 붙이지 않는다 (nodejs · go 와 동일)
            headers=self._bootpay.fixed_role_headers(self._bootpay.user_or_supervisor_role())
        )

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
            order_subscription_bill,
            headers=self._bootpay.fixed_role_headers('supervisor')
        )

    def _user_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        빌 조회 요청 헤더
        Idempotency-Key 는 미지정시 매 호출마다 생성된다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'user'
        }
