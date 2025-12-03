"""
Commerce API - Product Create (상품 생성) 테스트
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
    """상품 생성 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 이미지 없이 상품 생성
        response = commerce.product.create({
            'name': '테스트 상품',
            'price': 10000,
            'description': '테스트 상품 설명',
            'type': 1,
            'status': 1
        })
        print('=== Product Create Response ===')
        print(response)

        # 이미지와 함께 상품 생성
        # response_with_images = commerce.product.create(
        #     {
        #         'name': '테스트 상품 (이미지 포함)',
        #         'price': 20000,
        #         'description': '테스트 상품 설명',
        #         'type': 1
        #     },
        #     ['/path/to/image1.jpg', '/path/to/image2.jpg']
        # )
        # print('\n=== Product Create With Images Response ===')
        # print(response_with_images)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
