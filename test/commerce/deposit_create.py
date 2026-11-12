"""
Commerce API - 뱅크알람 입금대기 등록
POST /v1/sdk/deposits

판매자 입금 계좌가 등록돼 있어야 한다(18128).
"""

import time
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
    if not deposit_side_effect_allowed('deposit_create'):
        return

    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()
        response = commerce.deposit.create({
            'merchant_order_id': f'sdk-test-{time.time_ns()}',
            'price': 1000,
            'depositor': '홍길동'
        })
        print('=== Deposit Create Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
