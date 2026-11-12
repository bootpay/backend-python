"""Commerce API - 입점사 지급 요청 목록 (명시적 라이브 opt-in 전에는 실행하지 않음)."""
import os
import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from config import get_commerce_keys, payout_side_effect_allowed

keys = get_commerce_keys()


def main():
    if not payout_side_effect_allowed('payout_list'):
        return

    commerce = BootpayCommerce(
        client_key=keys['client_key'], secret_key=keys['secret_key'], mode=keys['mode']
    )
    commerce.get_access_token()
    status = os.getenv('BOOTPAY_TEST_PAYOUT_STATUS')
    print(commerce.payout.list({'status': status, 'page': 1, 'limit': 20}))


if __name__ == '__main__':
    main()
