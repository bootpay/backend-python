"""
Commerce API - 뱅크알람 입금대기 조회
GET /v1/sdk/deposits/{id}

id 는 가맹점 주문번호 또는 부트페이 주문번호다.
"""

import os
import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from config import get_commerce_keys

keys = get_commerce_keys()
CLIENT_KEY = keys['client_key']
SECRET_KEY = keys['secret_key']
MODE = keys['mode']


def main():
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()
        deposit_id = os.getenv('BOOTPAY_TEST_COMMERCE_DEPOSIT_ID', 'MERCHANT_ORDER_ID')
        print('=== Deposit Detail Response ===')
        print(commerce.deposit.detail(deposit_id))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
