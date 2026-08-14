"""
Commerce API - OrderSubscription Charge Revoke (수시결제 charge_key 해지) 테스트
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
    """수시결제(온디맨드) charge_key 해지 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        response = commerce.order_subscription.supervisor_charge_revoke({
            'charge_key': 'CHARGE_KEY_HERE'
        })
        print('=== OrderSubscription Charge Revoke Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
