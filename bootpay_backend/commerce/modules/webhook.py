import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import SendTestWebhookParams


class WebhookModule:
    """웹훅 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def send_test(self, params: Optional[SendTestWebhookParams] = None):
        """
        테스트 웹훅 발송
        POST /v1/webhook/test
        등록된 웹훅 URL 로 테스트 페이로드를 보내 연동을 확인할 때 쓴다.
        :param params: 발송 파라미터 (header_content_type 미지정시 전송하지 않는다)
        :return: 발송 결과
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        return self._bootpay.post(
            'webhook/test',
            self._compact(params),
            headers={'Idempotency-Key': idempotency_key or str(uuid.uuid4())}
        )

    def _compact(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """None 값을 제거한다."""
        return {k: v for k, v in payload.items() if v is not None}
