"""
Commerce API - OrderSubscription Update (정기구독 수정) 테스트
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
    """정기구독 수정 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # price 는 회차별 결제 기준금액이다. 바꾸면 결제예정(READY) 회차의 청구액이
        # 즉시 재계산되고 이후 회차도 이 금액으로 만들어진다 (이미 결제된 회차는 그대로).
        response = commerce.order_subscription.update({
            'order_subscription_id': 'ORDER_SUBSCRIPTION_ID_HERE',
            'order_name': '수정된 주문명',
            'price': 15000
        })
        print('=== OrderSubscription Update Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
