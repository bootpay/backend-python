import uuid
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource


class WebhookModule:
    """웹훅 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def _webhook_headers(self, idempotency_key: Optional[str] = None):
        """웹훅 전용 헤더 생성"""
        return {'Idempotency-Key': idempotency_key or str(uuid.uuid4())}

    def send_test_webhook(self, header_content_type: Optional[int] = None,
                          idempotency_key: Optional[str] = None):
        """
        테스트 웹훅 발송 (POST /v1/webhook/test)
        :param header_content_type: 웹훅 요청의 Content-Type 유형 (미지정시 서버 기본값)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 발송 결과
        """
        payload = {'header_content_type': header_content_type}
        return self._bootpay.post(
            'webhook/test',
            {key: value for key, value in payload.items() if value is not None},
            headers=self._webhook_headers(idempotency_key)
        )

    def send_test(self, header_content_type: Optional[int] = None,
                  idempotency_key: Optional[str] = None):
        return self.send_test_webhook(header_content_type, idempotency_key)
