"""
Commerce API - OrderSubscription Calculate Termination Fee (해지 위약금 계산) 테스트
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
    """해지 위약금 계산 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # order_subscription_id로 계산
        response = commerce.order_subscription.calculate_termination_fee(
            order_subscription_id='ORDER_SUBSCRIPTION_ID_HERE'
        )
        print('=== Calculate Termination Fee Response (by ID) ===')
        print(response)

        # order_number로 계산
        response2 = commerce.order_subscription.calculate_termination_fee_by_order_number(
            'ORDER_NUMBER_HERE'
        )
        print('\n=== Calculate Termination Fee Response (by Order Number) ===')
        print(response2)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
