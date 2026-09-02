from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    AlimtalkWebhookUpdateParams,
    AlimtalkWebhookDeliveryListParams
)


class AlimtalkWebhookModule:
    """
    알림톡 발송결과·검수결과 웹훅 설정 모듈 (/v1/alimtalk/webhook 계열)

    ⚠️ **주문·구독 통합 웹훅과 완전히 별개다.** 알림톡 이벤트를 기존 주문 웹훅 URL 로 태우면
       그 수신 서버가 모르는 payload 를 받아 기존 연동이 깨진다. 그래서 수신 URL 을 따로 둔다.
       (`webhook.send_test` 는 주문 웹훅용이다 — 이 모듈의 `test` 와 혼동하지 말 것)

    ## 서명 검증
    요청에 다음 헤더가 붙는다.
      X-Bootpay-Signature: sha256=HMAC_SHA256(secret, "{X-Bootpay-Timestamp}.{raw_body}")
    타임스탬프가 5분 이상 지난 요청은 거부한다 (replay 방지).
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def detail(self):
        """
        웹훅 설정 조회
        GET /v1/alimtalk/webhook
        시크릿은 앞 12자만 노출된다. 미설정이면 {'configured': False} 로 온다.
        :return: 웹훅 설정
        """
        return self._bootpay.get('alimtalk/webhook', headers=self._alimtalk_headers())

    def update(self, params: AlimtalkWebhookUpdateParams):
        """
        웹훅 설정 저장
        PUT /v1/alimtalk/webhook
        url 은 **https 만** 허용한다 (아니면 3028). 최초 저장 시 서명 시크릿이 자동 발급된다.
        events: 구독할 이벤트 코드. 목록에 없는 값은 저장 시 조용히 버려진다 (유령 구독 방지).
          300 발송 접수(기본 미구독) / 301 전달 성공 / 302 전달 실패 / 303 예약 취소 /
          304 문자(LMS) 대체발송 전환 / 310 검수 승인 / 311 검수 반려 / 320 수신거부 등록(기본 미구독)
        events 를 비우면 기본 구독셋(301·302·303·304·310·311)이 적용된다.
        :param params: 웹훅 설정
        :return: 저장된 웹훅 설정
        """
        return self._bootpay.put(
            'alimtalk/webhook',
            self._compact(params),
            headers=self._alimtalk_headers()
        )

    def test(self):
        """
        테스트 이벤트 1건 발송
        POST /v1/alimtalk/webhook/test
        ⚠️ **설정된 URL 로 실제 HTTP 요청이 나간다.** 구독 여부와 무관하게 보낸다.
        웹훅이 설정돼 있지 않으면 3029.
        :return: {'delivery_id':, 'url':, 'queued':}
        """
        return self._bootpay.post('alimtalk/webhook/test', headers=self._alimtalk_headers())

    def send_test(self):
        """test 별칭 (주문 웹훅 모듈의 send_test 와 이름을 맞춘 것 — 경로는 알림톡 전용이다)"""
        return self.test()

    def rotate_secret(self):
        """
        서명 시크릿 재발급
        POST /v1/alimtalk/webhook/secret
        ⚠️ **이 응답에서만 secret 원문을 돌려준다** (이후 조회는 마스킹된다).
        ⚠️ 이미 큐에 있는 전송 건은 발송 당시 시크릿으로 서명된다.
        :return: {'secret': ...}
        """
        return self._bootpay.post('alimtalk/webhook/secret', headers=self._alimtalk_headers())

    def deliveries(self, params: Optional[AlimtalkWebhookDeliveryListParams] = None):
        """
        웹훅 전송 이력 조회
        GET /v1/alimtalk/webhook/deliveries
        성공·실패를 모두 남긴다.
        :param params: 조회 파라미터 (limit 서버 기본 20, 최대 100)
        :return: {'list': [{'delivery_id':, 'event':, 'event_code':, 'url':, 'status':,
                            'retry_count':, 'max_retry':, 'tags':, 'created_at':}],
                  'count':, 'page':, 'per':}
        """
        query = urlencode(self._compact(params))
        return self._bootpay.get(
            f'alimtalk/webhook/deliveries{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def _compact(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        None 값을 제거한다.
        ⚠️ False 는 남긴다 — enabled: False 는 웹훅을 끄는 값이라 반드시 전달되어야 한다.
        """
        return {k: v for k, v in (params or {}).items() if v is not None}

    def _alimtalk_headers(self) -> Dict[str, str]:
        """
        알림톡 API 요청 헤더
        ★Idempotency-Key 를 싣지 않는다★ 알림톡 API 는 이 헤더를 읽지 않는다.
        ★BOOTPAY-ROLE 은 항상 user★ 알림톡 스코프 키가 전부 user:alimtalk_* 다.
        """
        return {'BOOTPAY-ROLE': 'user'}
