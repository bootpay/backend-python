from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceOrderSubscriptionAdjustment,
    OrderSubscriptionAdjustmentUpdateParams
)


class OrderSubscriptionAdjustmentModule:
    """정기구독 조정 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def create(self, order_subscription_id: str, adjustment: CommerceOrderSubscriptionAdjustment):
        """
        정기구독 조정 생성
        :param order_subscription_id: 정기구독 ID
        :param adjustment: 조정 정보
        :return: CommerceOrderSubscriptionAdjustment
        """
        return self._bootpay.post(
            f'order_subscriptions/{order_subscription_id}/adjustments',
            adjustment
        )

    def update(self, params: OrderSubscriptionAdjustmentUpdateParams):
        """
        정기구독 조정 수정
        :param params: 수정 파라미터
        :return: CommerceOrderSubscriptionAdjustment
        """
        if not params.get('order_subscription_id'):
            raise ValueError('order_subscription_id is required')
        return self._bootpay.put(
            f'order_subscriptions/{params["order_subscription_id"]}/adjustments',
            params
        )

    def delete(self, order_subscription_id: str, order_subscription_adjustment_id: str):
        """
        정기구독 조정 삭제
        :param order_subscription_id: 정기구독 ID
        :param order_subscription_adjustment_id: 조정 ID
        :return: None
        """
        return self._bootpay.delete(
            f'order_subscriptions/{order_subscription_id}/adjustments?order_subscription_adjustment_id={order_subscription_adjustment_id}'
        )
