"""
Commerce API - UserGroup Aggregate Transaction (그룹 거래 집계) 테스트
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
    """그룹 거래 집계 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        response = commerce.user_group.aggregate_transaction({
            'user_group_id': 'USER_GROUP_ID_HERE',
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        })
        print('=== UserGroup Aggregate Transaction Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
