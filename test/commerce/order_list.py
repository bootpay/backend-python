"""
Commerce API - Order List (주문 목록 조회) 테스트
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
    """주문 목록 조회 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 기본 목록 조회
        response = commerce.order.list()
        print('=== Order List Response ===')
        print(response)

        # 파라미터로 조회
        filtered_response = commerce.order.list({
            'page': 1,
            'limit': 10,
            'keyword': '주문',
            'user_id': 'USER_ID_HERE',
            'status': [1, 2]
        })
        print('\n=== Filtered Order List Response ===')
        print(filtered_response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
