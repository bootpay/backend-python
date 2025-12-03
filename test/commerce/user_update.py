"""
Commerce API - User Update (사용자 정보 수정) 테스트
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
    """사용자 정보 수정 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        response = commerce.user.update({
            'user_id': 'USER_ID_HERE',
            'name': '수정된 이름',
            'email': 'updated@example.com',
            'phone': '010-9876-5432'
        })
        print('=== User Update Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
