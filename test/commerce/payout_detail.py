"""Commerce API - 입점사 지급 요청 조회 (명시적 라이브 opt-in 전에는 실행하지 않음)."""
import os
import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from config import get_commerce_keys, payout_side_effect_allowed

keys = get_commerce_keys()


def main():
    if not payout_side_effect_allowed('payout_detail'):
        return

    commerce = BootpayCommerce(
        client_key=keys['client_key'], secret_key=keys['secret_key'], mode=keys['mode']
    )
    commerce.get_access_token()
    payout_id = os.getenv('BOOTPAY_TEST_PAYOUT_ID', 'PAYOUT_ID')
    print(commerce.payout.detail(payout_id))


if __name__ == '__main__':
    main()
