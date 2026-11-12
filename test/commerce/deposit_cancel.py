"""
Commerce API - 뱅크알람 입금대기 취소
DELETE /v1/sdk/deposits/{id}

이미 닫힌 주문은 그대로 돌려준다.
"""

import os
import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from config import get_commerce_keys, deposit_side_effect_allowed

keys = get_commerce_keys()
CLIENT_KEY = keys['client_key']
SECRET_KEY = keys['secret_key']
MODE = keys['mode']


def main():
    if not deposit_side_effect_allowed('deposit_cancel'):
        return

    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()
        deposit_id = os.getenv('BOOTPAY_TEST_COMMERCE_DEPOSIT_ID', 'MERCHANT_ORDER_ID')
        print('=== Deposit Cancel Response ===')
        print(commerce.deposit.cancel(deposit_id))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
