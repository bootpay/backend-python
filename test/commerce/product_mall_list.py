"""
Commerce API - Product Mall List (V1 Mall API 상품 목록 / 상세 조회) 테스트
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

# 회원 로그인시 발급받은 JWT (비회원 조회시 None)
USER_JWT = None


def main():
    """Mall API 상품 목록 / 상세 조회 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        products = commerce.product.products({
            'page': 1,
            'limit': 20
        }, user_jwt=USER_JWT)
        print('=== Product Mall List Response ===')
        print(products)

        detail = commerce.product.product_detail('PRODUCT_ID_HERE', user_jwt=USER_JWT)
        print('=== Product Mall Detail Response ===')
        print(detail)

        lookup = commerce.product.lookup_product('PRODUCT_ID_HERE')
        print('=== Product Lookup Response ===')
        print(lookup)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
