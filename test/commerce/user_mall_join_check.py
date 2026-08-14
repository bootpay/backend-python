"""
Commerce API - User Mall Join Check (V1 Mall API 회원가입 중복 확인) 테스트
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
    """회원가입 중복 확인 테스트 (GET user/join/{type}?pk=)"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # email-exist, id-exist, phone-exist, group-business-number-exist
        response = commerce.user.user_join_check('email-exist', 'test_user@example.com')
        print('=== User Mall Join Check Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
