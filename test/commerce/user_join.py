"""
Commerce API - User Join (회원가입) 테스트
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
    """회원가입 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        response = commerce.user.join({
            'login_id': 'test_user@example.com',
            'login_pw': 'password123',
            'name': '테스트 사용자',
            'email': 'test_user@example.com',
            'phone': '010-1234-5678'
        })
        print('=== User Join Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
