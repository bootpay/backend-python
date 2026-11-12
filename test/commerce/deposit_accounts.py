"""
Commerce API - 뱅크알람 입금 계좌 목록
GET /v1/sdk/deposits/accounts
"""

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
        print('=== Deposit Accounts Response ===')
        print(commerce.deposit.accounts())
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
