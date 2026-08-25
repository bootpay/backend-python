"""
Commerce API - OrderSubscriptionAdjustment Create (정기구독 조정 생성) 테스트
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
    """정기구독 조정 생성 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 단일 회차 — 5회차 한 건만
        response = commerce.order_subscription_adjustment.create(
            'ORDER_SUBSCRIPTION_ID_HERE',
            {
                'name': '설치비',
                'price': 5000,
                'duration': 5,
                'tax_free_price': 0
            }
        )
        print('=== OrderSubscriptionAdjustment Create Response ===')
        print(response)

        # 회차 범위 — 3~7회차 각각 한 건씩 (총 5건)
        response = commerce.order_subscription_adjustment.create(
            'ORDER_SUBSCRIPTION_ID_HERE',
            {
                'name': '기간할인',
                'price': -1000,
                'duration_from': 3,
                'duration_to': 7
            }
        )
        print('=== OrderSubscriptionAdjustment Create (range) Response ===')
        print(response)

        # 무제한 범위 — 3회차부터 계약 끝까지 (레코드는 1건, duration_to 는 무시된다)
        response = commerce.order_subscription_adjustment.create(
            'ORDER_SUBSCRIPTION_ID_HERE',
            {
                'name': '무기한할인',
                'price': -500,
                'duration_from': 3,
                'is_unlimited': True
            }
        )
        print('=== OrderSubscriptionAdjustment Create (unlimited) Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
