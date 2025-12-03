"""
Commerce API - OrderSubscriptionAdjustment Update (정기구독 조정 수정) 테스트
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
    """정기구독 조정 수정 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        response = commerce.order_subscription_adjustment.update({
            'order_subscription_id': 'ORDER_SUBSCRIPTION_ID_HERE',
            'order_subscription_adjustment_id': 'ORDER_SUBSCRIPTION_ADJUSTMENT_ID_HERE',
            'amount': 10000,
            'reason': '수정된 할인 금액'
        })
        print('=== OrderSubscriptionAdjustment Update Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
