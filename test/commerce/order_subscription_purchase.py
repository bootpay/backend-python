"""
Commerce API - 정기구독 중도인수 요청 테스트
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
    """정기구독 중도인수 요청 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        response = commerce.order_subscription.purchase({
            'order_subscription_id': 'ORDER_SUBSCRIPTION_ID_HERE',
            'price': 10000,
            'tax_free_price': 0,
            'reason': '중도인수 사유'
        })
        print('=== OrderSubscription Purchase Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
