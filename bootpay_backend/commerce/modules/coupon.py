from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceCoupon,
    CouponListParams,
    CouponDownloadParams
)


class CouponModule:
    """쿠폰 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[CouponListParams] = None):
        """
        사용자 보유 쿠폰 목록 조회
        :param params: 조회 파라미터
        :return: List[CommerceCoupon]
        """
        query_params = {}
        if params:
            if params.get('status'):
                query_params['status'] = params['status']
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'coupon{"?" + query if query else ""}')

    def available(self):
        """
        다운로드 가능한 쿠폰 목록
        :return: List[CommerceCoupon]
        """
        return self._bootpay.get('coupon/available')

    def download(self, params: CouponDownloadParams):
        """
        쿠폰 다운로드 (issue_from_template)
        :param params: {'coupon_template_id': str}
        :return: CommerceCoupon
        """
        return self._bootpay.post('coupon/download', params)
