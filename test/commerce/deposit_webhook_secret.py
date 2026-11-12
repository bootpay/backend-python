"""
Commerce API - 뱅크알람 웹훅 서명 비밀값 발급
POST /v1/sdk/deposits/webhook_secret

⚠️ 부를 때마다 비밀값이 바뀌며, 원문은 이 응답에서만 받을 수 있다.
"""

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
    if not deposit_side_effect_allowed('deposit_webhook_secret'):
        return

    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()
        print('=== Deposit Webhook Secret Response ===')
        print(commerce.deposit.webhook_secret())
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
