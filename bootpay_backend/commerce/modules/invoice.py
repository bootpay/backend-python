import uuid
from typing import TYPE_CHECKING, Optional, List, Dict
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceInvoice,
    InvoiceListParams,
    InvoiceListResponse,
    ListParams
)


class InvoiceModule:
    """청구서 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[InvoiceListParams] = None):
        """
        청구서 목록 조회
        GET /v1/invoices
        응답은 {'list': [...], 'count': N} 구조다 ({'items', 'total'} 아님).
        limit 미지정시 서버 기본값과 동일한 24 를 보낸다.
        :param params: 조회 파라미터
        :return: InvoiceListResponse — {'list': List[CommerceInvoice], 'count': int}
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)

        query_params = {
            'page': 1 if params.get('page') is None else params['page'],
            'limit': 24 if params.get('limit') is None else params['limit'],
        }
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

        return self._bootpay.get(
            f'invoices?{urlencode(query_params)}',
            headers=self._invoice_headers(idempotency_key)
        )

    def create(self, invoice: CommerceInvoice):
        """
        청구서 생성
        :param invoice: 청구서 정보
        :return: CommerceInvoice
        """
        return self._bootpay.post('invoices', invoice)

    def notify(self, invoice_id: str, send_types: Optional[List[int]] = None,
               idempotency_key: Optional[str] = None):
        """
        청구서 알림 재발송
        POST /v1/invoices/{invoice_id}/notify
        send_types 미전달시 서버가 빈 배열로 처리한다.
        ⚠️ 실제 고객에게 알림이 발송되므로 테스트 호출 주의.
        :param invoice_id: 청구서 ID
        :param send_types: 발송 타입 배열 (예: [1, 2] - SMS, Email 등)
        :param idempotency_key: 미지정시 자동 생성
        :return: None
        """
        payload = {}
        if send_types is not None:
            payload['send_types'] = send_types
        return self._bootpay.post(
            f'invoices/{invoice_id}/notify',
            payload,
            headers=self._invoice_headers(idempotency_key)
        )

    def detail(self, invoice_id: str, idempotency_key: Optional[str] = None):
        """
        청구서 상세 조회
        GET /v1/invoices/{invoice_id}
        :param invoice_id: 청구서 ID
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceInvoice
        """
        return self._bootpay.get(
            f'invoices/{invoice_id}',
            headers=self._invoice_headers(idempotency_key)
        )

    def _invoice_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        청구서 API 요청 헤더
        Idempotency-Key 는 미지정시 매 호출마다 생성된다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'user'
        }
