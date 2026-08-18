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

    def list(self, params: Optional[InvoiceListParams] = None):
        """
        청구서 목록 조회 (GET /v1/invoices)
        응답은 {'list': [...], 'count': N} 구조이며 서버 기본 limit은 24이다.
        :param params: 조회 파라미터 (page, limit, keyword, cs_type, user_id, product_type,
                       css_at, cse_at)
        :return: {'list': List[CommerceInvoice], 'count': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']
            if params.get('cs_type'):
                query_params['cs_type'] = params['cs_type']
            if params.get('user_id'):
                query_params['user_id'] = params['user_id']
            if params.get('product_type') is not None:
                query_params['product_type'] = params['product_type']
            if params.get('css_at'):
                query_params['css_at'] = params['css_at']
            if params.get('cse_at'):
                query_params['cse_at'] = params['cse_at']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'invoices{"?" + query if query else ""}')

    def create(self, invoice: CommerceInvoice):
        """
        청구서 생성
        :param invoice: 청구서 정보
        :return: CommerceInvoice
        """
        return self._bootpay.post('invoices', invoice)

    def notify(self, invoice_id: str, send_types: Optional[List[int]] = None):
        """
        청구서 재안내(알림 발송) (POST /v1/invoices/:id/notify)
        send_types 미지정시 서버가 빈 배열로 처리한다.
        실제 고객에게 알림이 발송되므로 테스트 호출에 주의한다.
        :param invoice_id: 청구서 ID
        :param send_types: 발송 타입 배열 (예: [1, 2] - SMS, Email 등)
        :return: None
        """
        payload = {'send_types': send_types} if send_types is not None else {}
        return self._bootpay.post(f'invoices/{invoice_id}/notify', payload)

    def detail(self, invoice_id: str):
        """
        청구서 상세 조회
        :param invoice_id: 청구서 ID
        :return: CommerceInvoice
        """
        return self._bootpay.get(f'invoices/{invoice_id}')
