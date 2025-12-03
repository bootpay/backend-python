from typing import TYPE_CHECKING, Optional, List
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceInvoice,
    InvoiceListParams,
    ListParams
)


class InvoiceModule:
    """청구서 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[ListParams] = None):
        """
        청구서 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceInvoice], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'invoices{"?" + query if query else ""}')

    def create(self, invoice: CommerceInvoice):
        """
        청구서 생성
        :param invoice: 청구서 정보
        :return: CommerceInvoice
        """
        return self._bootpay.post('invoices', invoice)

    def notify(self, invoice_id: str, send_types: List[int]):
        """
        청구서 알림 발송
        :param invoice_id: 청구서 ID
        :param send_types: 발송 타입 배열 (예: [1, 2] - SMS, Email 등)
        :return: None
        """
        return self._bootpay.post(f'invoices/{invoice_id}/notify', {'send_types': send_types})

    def detail(self, invoice_id: str):
        """
        청구서 상세 조회
        :param invoice_id: 청구서 ID
        :return: CommerceInvoice
        """
        return self._bootpay.get(f'invoices/{invoice_id}')
