"""
Commerce API - User Session (회원 세션 조회 / 로그아웃) 테스트
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

# 회원 로그인시 발급받은 JWT
USER_JWT = 'USER_JWT_HERE'


def main():
    """회원 세션 조회 후 로그아웃 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        session = commerce.user.user_session(user_jwt=USER_JWT)
        print('=== User Session Response ===')
        print(session)

        logout = commerce.user.user_logout(user_jwt=USER_JWT)
        print('=== User Logout Response ===')
        print(logout)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
