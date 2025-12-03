"""
Commerce API 기본 테스트

config.py의 CURRENT_ENV를 변경하여 환경을 선택할 수 있습니다.
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


def test_get_access_token():
    """토큰 발급 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    response = commerce.get_access_token()
    print('=== 토큰 발급 ===')
    print(response)

    # 토큰이 설정되었는지 확인
    assert commerce.has_token(), "토큰이 설정되지 않았습니다."
    print(f'Current Token: {commerce.get_current_token()[:20]}...')


def test_user_list():
    """사용자 목록 조회 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )
    commerce.get_access_token()

    response = commerce.user.list({
        'page': 1,
        'limit': 10
    })
    print('=== 사용자 목록 ===')
    print(response)


def test_product_list():
    """상품 목록 조회 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )
    commerce.get_access_token()

    response = commerce.product.list({
        'page': 1,
        'limit': 10
    })
    print('=== 상품 목록 ===')
    print(response)


def test_order_list():
    """주문 목록 조회 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )
    commerce.get_access_token()

    response = commerce.order.list({
        'page': 1,
        'limit': 10
    })
    print('=== 주문 목록 ===')
    print(response)


def test_role_chaining():
    """Role 체이닝 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    # 체이닝 테스트
    commerce.as_manager()
    assert commerce.get_current_role() == 'manager'

    commerce.as_user()
    assert commerce.get_current_role() == 'user'

    commerce.as_supervisor()
    assert commerce.get_current_role() == 'supervisor'

    commerce.clear_role()
    assert commerce.get_current_role() == 'user'

    print('=== Role 체이닝 테스트 통과 ===')


def test_with_token_chaining():
    """토큰 체이닝 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    # 체이닝으로 토큰 발급
    result = commerce.with_token()
    assert result is commerce
    assert commerce.has_token()

    print('=== 토큰 체이닝 테스트 통과 ===')


if __name__ == '__main__':
    print(f'Commerce API 기본 테스트 (환경: {MODE})\n')

    # Role 체이닝 테스트 (API 호출 없이 진행 가능)
    test_role_chaining()

    # 실제 API 테스트
    test_get_access_token()
    test_user_list()
    test_product_list()
    test_order_list()
    test_with_token_chaining()

    print('\n테스트 완료!')
