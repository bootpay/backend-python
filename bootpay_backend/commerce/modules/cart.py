from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    OrderPreviewParams,
    OrderPreviewResponse
)


class CartModule:
    """장바구니 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def order_preview(self, params: Optional[OrderPreviewParams] = None):
        """
        주문 미리보기 (배송비/할인 권위적 계산)
        POST /v1/cart/order-preview

        member_mode='guest' (기본): cart_items 필수
        member_mode='member': 서버 장바구니 사용 (user 토큰 필요)

        :param params: 주문 미리보기 파라미터
        :return: OrderPreviewResponse
        """
        return self._bootpay.post('cart/order-preview', params if params is not None else {})
