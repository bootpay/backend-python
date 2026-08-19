import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceOrderSubscriptionAdjustment,
    OrderSubscriptionAdjustmentUpdateParams
)


class OrderSubscriptionAdjustmentModule:
    """
    구독 가감산 조정항목 모듈

    ⚠️ /adjustments 한 경로에 POST · PUT · DELETE 세 동사가 걸려 있다.
       경로만 보고 메서드를 유추하지 말 것.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def create(self, order_subscription_id: str, adjustment: CommerceOrderSubscriptionAdjustment,
               idempotency_key: Optional[str] = None):
        """
        가감산 조정항목 추가
        POST /v1/order_subscriptions/{order_subscription_id}/adjustments
        type 미전달시 서버가 price > 0 이면 SETUP_PRICE, 아니면 PERIOD_DISCOUNT 로 자동 판정한다.
        :param order_subscription_id: 정기구독 ID
        :param adjustment: 조정 정보 (price/duration/tax_free_price 미지정시 각각 0 / 1 / 0)
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceOrderSubscriptionAdjustment
        """
        payload = {'price': 0, 'duration': 1, 'tax_free_price': 0}
        payload.update(adjustment or {})
        payload = self._compact(payload)
        return self._bootpay.post(
            f'order_subscriptions/{order_subscription_id}/adjustments',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def update(self, params: OrderSubscriptionAdjustmentUpdateParams):
        """
        특정 회차의 조정항목을 통째로 교체
        PUT /v1/order_subscriptions/{order_subscription_id}/adjustments
        서버는 duration(회차) 단위로 adjustments 배열을 갈아끼운다. duration 미지정시 1 이 적용된다.
        :param params: 수정 파라미터
        :return: CommerceOrderSubscriptionAdjustment
        """
        if not params.get('order_subscription_id'):
            raise ValueError('order_subscription_id is required')
        params = dict(params)
        order_subscription_id = params.pop('order_subscription_id')
        idempotency_key = params.pop('idempotency_key', None)
        payload = {'duration': 1}
        payload.update(params)
        payload = self._compact(payload)
        return self._bootpay.put(
            f'order_subscriptions/{order_subscription_id}/adjustments',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def delete(self, order_subscription_id: str, order_subscription_adjustment_id: str,
               idempotency_key: Optional[str] = None):
        """
        조정항목 삭제
        DELETE /v1/order_subscriptions/{order_subscription_id}/adjustments
        ⚠️ 대상 ID 는 query 가 아니라 body 로 보낸다.
        :param order_subscription_id: 정기구독 ID
        :param order_subscription_adjustment_id: 조정 ID
        :param idempotency_key: 미지정시 자동 생성
        :return: None
        """
        return self._bootpay.delete(
            f'order_subscriptions/{order_subscription_id}/adjustments',
            data={'order_subscription_adjustment_id': order_subscription_adjustment_id},
            headers=self._supervisor_headers(idempotency_key)
        )

    def _compact(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """None 값을 제거한다."""
        return {k: v for k, v in payload.items() if v is not None}

    def _supervisor_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        조정항목 API 요청 헤더 — 서버가 supervisor scope 를 요구한다.
        Idempotency-Key 는 미지정시 매 호출마다 생성된다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }
