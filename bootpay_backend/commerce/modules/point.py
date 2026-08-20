from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    PointBalance,
    PointTransactionsParams,
    PointTransactionsResponse
)


class PointModule:
    """적립금 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def balance(self):
        """
        적립금 잔액 조회
        :return: PointBalance
        """
        return self._bootpay.get('point/balance')

    def transactions(self, params: Optional[PointTransactionsParams] = None):
        """
        적립금 내역 조회
        :param params: 조회 파라미터
        :return: PointTransactionsResponse
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('transaction_type') is not None:
                query_params['transaction_type'] = params['transaction_type']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'point/transactions{"?" + query if query else ""}')
