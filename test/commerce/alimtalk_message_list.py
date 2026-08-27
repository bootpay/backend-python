"""
Commerce API - Alimtalk Message List (알림톡 발송내역 조회) 테스트
"""

import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from config import get_commerce_keys

# 환경에 맞는 키 가져오기
keys = get_commerce_keys()
CLIENT_KEY = keys['client_key']
SECRET_KEY = keys['secret_key']
MODE = keys['mode']


def main():
    """알림톡 발송내역 조회 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 유료 알림톡만 조회된다 (무료 커머스 알림톡은 포함되지 않는다).
        # 기간 기본값은 최근 30일, 최대 조회 폭은 92일 — 초과분은 시작일을 당겨 잘라내므로
        # 실제 적용된 구간은 응답의 period 로 확인한다.
        response = commerce.alimtalk_message.list({
            'status': 'success',
            'page': 1,
            'limit': 20
        })
        print('=== Alimtalk Message List Response ===')
        print(response)

        # 기간 집계 — 일자별 집계 원장에서 읽으므로 빠르다.
        # billing.unit_price_source 가 'default' 면 잠정 단가다 (확정 청구액이 아니다).
        stats = commerce.alimtalk_message.stats({'s_at': '2026-08-01', 'e_at': '2026-08-27'})
        print('\n=== Alimtalk Message Stats Response ===')
        print(stats)

        # 단건 발송 결과 — 실패 사유는 error_code·error_message 에 담긴다.
        detail = commerce.alimtalk_message.detail('RECEIPT_ID_HERE')
        print('\n=== Alimtalk Message Detail Response ===')
        print(detail)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
