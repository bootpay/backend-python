"""
Commerce API - Alimtalk Webhook (알림톡 웹훅 설정) 테스트

⚠️ 주문·구독 통합 웹훅과 완전히 별개다. 알림톡 이벤트를 기존 주문 웹훅 URL 로 태우면
   그 수신 서버가 모르는 payload 를 받아 기존 연동이 깨진다.

서명 검증: X-Bootpay-Signature: sha256=HMAC_SHA256(secret, "{X-Bootpay-Timestamp}.{raw_body}")
          타임스탬프가 5분 이상 지난 요청은 거부한다 (replay 방지).
"""

import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from bootpay_backend.commerce import (
    ALIMTALK_WEBHOOK_EVENT_SEND_SUCCESS,
    ALIMTALK_WEBHOOK_EVENT_SEND_FAILED,
    ALIMTALK_WEBHOOK_EVENT_TEMPLATE_APPROVED,
    ALIMTALK_WEBHOOK_EVENT_TEMPLATE_REJECTED
)
from config import get_commerce_keys

# 환경에 맞는 키 가져오기
keys = get_commerce_keys()
CLIENT_KEY = keys['client_key']
SECRET_KEY = keys['secret_key']
MODE = keys['mode']


def main():
    """알림톡 웹훅 설정 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # url 은 https 만 허용한다 (아니면 3028). 최초 저장 시 서명 시크릿이 자동 발급된다.
        # events 목록에 없는 값은 저장 시 조용히 버려진다 (유령 구독 방지).
        response = commerce.alimtalk_webhook.update({
            'url': 'https://example.com/alimtalk/webhook',
            'events': [
                ALIMTALK_WEBHOOK_EVENT_SEND_SUCCESS,
                ALIMTALK_WEBHOOK_EVENT_SEND_FAILED,
                ALIMTALK_WEBHOOK_EVENT_TEMPLATE_APPROVED,
                ALIMTALK_WEBHOOK_EVENT_TEMPLATE_REJECTED
            ],
            'enabled': True
        })
        print('=== Alimtalk Webhook Update Response ===')
        print(response)

        # 시크릿은 앞 12자만 노출된다. 미설정이면 {'configured': False} 로 온다.
        print('\n=== Alimtalk Webhook Detail Response ===')
        print(commerce.alimtalk_webhook.detail())

        # ⚠️ 설정된 URL 로 실제 HTTP 요청이 나간다 (구독 여부와 무관).
        print('\n=== Alimtalk Webhook Test Response ===')
        print(commerce.alimtalk_webhook.test())

        # ⚠️ 이 응답에서만 secret 원문을 돌려준다 (이후 조회는 마스킹된다).
        print('\n=== Alimtalk Webhook Rotate Secret Response ===')
        print(commerce.alimtalk_webhook.rotate_secret())

        print('\n=== Alimtalk Webhook Deliveries Response ===')
        print(commerce.alimtalk_webhook.deliveries({'page': 1, 'limit': 20}))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
