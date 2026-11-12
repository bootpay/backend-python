"""Commerce API - 입점사 지급 요청 등록 (명시적 라이브 opt-in 전에는 실행하지 않음)."""
import os
import time
import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from config import get_commerce_keys, payout_side_effect_allowed

keys = get_commerce_keys()


def main():
    if not payout_side_effect_allowed('payout_create'):
        return

    commerce = BootpayCommerce(
        client_key=keys['client_key'], secret_key=keys['secret_key'], mode=keys['mode']
    )
    commerce.get_access_token()
    print(commerce.payout.create({
        'sub_seller_id': os.getenv('BOOTPAY_TEST_PAYOUT_SUB_SELLER_ID', 'SUB_SELLER_ID'),
        'amount': 1,
        'merchant_payout_id': f'sdk-test-payout-{time.time_ns()}',
        'payout_date': os.getenv('BOOTPAY_TEST_PAYOUT_DATE') or None,
    }))


if __name__ == '__main__':
    main()
