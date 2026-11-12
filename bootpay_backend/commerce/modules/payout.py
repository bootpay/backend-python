import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any, List
from urllib.parse import quote

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import CommercePayout, PayoutCreateParams, PayoutListParams


class PayoutModule:
    """입점사 지급 요청 모듈 (/v1/sdk/payouts)."""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def create(self, params: PayoutCreateParams) -> CommercePayout:
        """입점사와 지급액을 지정해 지급 원장에 등록한다."""
        payload = self._compact({k: v for k, v in params.items() if k != 'idempotency_key'})
        return self._bootpay.post(
            'sdk/payouts', payload,
            headers=self._supervisor_headers(params.get('idempotency_key'))
        )

    def detail(self, payout_id: str, idempotency_key: Optional[str] = None) -> CommercePayout:
        """merchant_payout_id 또는 지급 항목 id로 한 건을 조회한다."""
        if not payout_id:
            raise ValueError('payout_id is required')
        return self._bootpay.get(
            f'sdk/payouts/{quote(payout_id, safe="")}',
            headers=self._supervisor_headers(idempotency_key)
        )

    def list(self, params: Optional[PayoutListParams] = None) -> List[CommercePayout]:
        """현재 프로젝트의 지급 항목 배열을 최근 생성 순으로 조회한다."""
        request_params = params or {}
        query = self._compact({k: v for k, v in request_params.items() if k != 'idempotency_key'})
        return self._bootpay.get(
            'sdk/payouts', params=query,
            headers=self._supervisor_headers(request_params.get('idempotency_key'))
        )

    def _compact(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """None 값을 제거한다 (0과 빈 문자열은 호출자가 보낸 값으로 유지한다)."""
        return {k: v for k, v in payload.items() if v is not None}

    def _supervisor_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """요청별 supervisor 헤더와 멱등키 (미지정시 매 호출마다 UUID 생성)."""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }
