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


def test_basic_auth_not_cached_as_token():
    """Basic 인증값이 토큰으로 저장되지 않는지 테스트 (API 호출 없이 진행 가능)"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    # 토큰이 없을 경우 매 요청마다 Basic 인증 헤더를 사용해야 한다
    first = commerce._get_headers()
    second = commerce._get_headers()

    assert first['Authorization'].startswith('Basic '), first['Authorization']
    assert second['Authorization'] == first['Authorization']

    # Basic 인증값이 토큰으로 저장되면 이후 요청이 Bearer로 잘못 전송된다
    assert not commerce.has_token()

    print('=== Basic 인증 캐싱 테스트 통과 ===')


def test_mall_api_endpoints():
    """V1 Mall API 요청 정보 테스트 (API 호출 없이 진행 가능)"""
    from unittest.mock import patch

    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    requested = {}

    class DummyResponse:
        def json(self):
            return {}

    def record(url, **kwargs):
        requested['url'] = url
        requested.update(kwargs)
        return DummyResponse()

    with patch('requests.post', record):
        commerce.user.user_login('test_user@example.com', 'password123', corporate_type=1)

    assert requested['url'].endswith('/user/login'), requested['url']
    assert requested['json'] == {
        'login_id': 'test_user@example.com',
        'password': 'password123',
        'corporate_type': 1
    }
    assert requested['headers']['Idempotency-Key']

    with patch('requests.get', record):
        commerce.user.user_join_check('email-exist', 'test_user@example.com')

    assert requested['url'].endswith('/user/join/email-exist'), requested['url']
    assert requested['params'] == {'pk': 'test_user@example.com'}

    with patch('requests.get', record):
        commerce.product.products({'page': 1, 'limit': 20, 'category_id': 'CATEGORY_ID'}, user_jwt='USER_JWT')

    assert requested['url'].endswith('/products'), requested['url']
    assert requested['params'] == {'page': 1, 'limit': 20, 'category_id': 'CATEGORY_ID'}
    assert requested['headers']['Bootpay-User-JWT'] == 'USER_JWT'

    with patch('requests.get', record):
        commerce.store.get_store(idempotency_key='IDEMPOTENCY_KEY')

    assert requested['url'].endswith('/store'), requested['url']
    assert requested['headers']['Idempotency-Key'] == 'IDEMPOTENCY_KEY'

    print('=== Mall API 엔드포인트 테스트 통과 ===')


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
    test_basic_auth_not_cached_as_token()
    test_mall_api_endpoints()

    # 실제 API 테스트
    test_get_access_token()
    test_user_list()
    test_product_list()
    test_order_list()
    test_with_token_chaining()

    print('\n테스트 완료!')
