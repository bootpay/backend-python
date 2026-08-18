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
    """V1 API 요청 정보 테스트 (API 호출 없이 진행 가능)"""
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

    assert requested['url'].endswith('/users/login'), requested['url']
    assert requested['json'] == {
        'login_id': 'test_user@example.com',
        'password': 'password123',
        'corporate_type': 1
    }
    assert requested['headers']['Idempotency-Key']

    with patch('requests.get', record):
        commerce.user.user_join_check('email-exist', 'test_user@example.com')

    assert requested['url'].endswith('/users/join/email-exist'), requested['url']
    assert requested['params'] == {'pk': 'test_user@example.com'}

    with patch('requests.get', record):
        commerce.user.user_session(user_jwt='USER_JWT')

    assert requested['url'].endswith('/users/session'), requested['url']
    assert requested['headers']['Bootpay-User-JWT'] == 'USER_JWT'

    with patch('requests.delete', record):
        commerce.user.user_logout(user_jwt='USER_JWT')

    assert requested['url'].endswith('/users/session'), requested['url']

    with patch('requests.post', record):
        commerce.user.user_join({
            'login_id': 'test_user@example.com',
            'password': 'password123',
            'name': '홍길동'
        })

    assert requested['url'].endswith('/users/join'), requested['url']

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


def test_commerce_endpoints():
    """신규 Commerce API 요청 정보 테스트 (API 호출 없이 진행 가능)"""
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
        requested.clear()
        requested['url'] = url
        requested.update(kwargs)
        return DummyResponse()

    # 테스트 웹훅 발송
    with patch('requests.post', record):
        commerce.webhook.send_test_webhook(header_content_type=1)

    assert requested['url'].endswith('/webhook/test'), requested['url']
    assert requested['json'] == {'header_content_type': 1}
    assert requested['headers']['Idempotency-Key']

    # 구독 중도인수 요청
    with patch('requests.post', record):
        commerce.order_subscription.purchase({
            'order_subscription_id': 'ORDER_SUBSCRIPTION_ID',
            'price': 10000,
            'tax_free_price': 0,
            'reason': '중도인수'
        })

    assert requested['url'].endswith('/order_subscriptions/requests/ing/purchase'), requested['url']
    assert requested['json']['order_subscription_id'] == 'ORDER_SUBSCRIPTION_ID'

    # 구독 이전/승계 요청
    with patch('requests.post', record):
        commerce.order_subscription.transfer({
            'order_subscription_id': 'ORDER_SUBSCRIPTION_ID',
            'new_user_id': 'NEW_USER_ID'
        })

    assert requested['url'].endswith('/order_subscriptions/requests/ing/transfer'), requested['url']
    assert requested['json']['new_user_id'] == 'NEW_USER_ID'

    # 구독 재개 요청은 PUT 이다 (requests/ing 계열 중 유일)
    with patch('requests.put', record):
        commerce.order_subscription.resume({'order_subscription_id': 'ORDER_SUBSCRIPTION_ID'})

    assert requested['url'].endswith('/order_subscriptions/requests/ing/resume'), requested['url']

    # 중도해지 수수료 사전계산 (두 인자 모두 전달 가능)
    with patch('requests.get', record):
        commerce.order_subscription.calculate_termination_fee(
            order_subscription_id='ORDER_SUBSCRIPTION_ID',
            order_number='ORDER_NUMBER'
        )

    assert 'order_subscription_id=ORDER_SUBSCRIPTION_ID' in requested['url'], requested['url']
    assert 'order_number=ORDER_NUMBER' in requested['url'], requested['url']

    # 구독 변경요청 목록 (project_id 지정시 supervisor)
    with patch('requests.get', record):
        commerce.order_subscription_request.list({'project_id': 'PROJECT_ID'})

    assert requested['url'].endswith('/order-subscription-requests'), requested['url']
    assert requested['params']['project_id'] == 'PROJECT_ID'
    assert requested['headers']['BOOTPAY-ROLE'] == 'supervisor'

    with patch('requests.get', record):
        commerce.order_subscription_request.list()

    assert requested['headers']['BOOTPAY-ROLE'] == 'user'

    # 구독 변경요청 상세
    with patch('requests.get', record):
        commerce.order_subscription_request.detail('REQUEST_HISTORY_ID')

    assert requested['url'].endswith('/order-subscription-requests/REQUEST_HISTORY_ID'), requested['url']

    # 구독 변경요청 승인/반려는 approval 값으로 구분한다
    with patch('requests.put', record):
        commerce.order_subscription_request.update({
            'request_history_id': 'REQUEST_HISTORY_ID',
            'approval': 'approve',
            'reason': '승인'
        })

    assert requested['url'].endswith('/order-subscription-requests/REQUEST_HISTORY_ID'), requested['url']
    assert requested['json'] == {'approval': 'approve', 'reason': '승인'}
    assert requested['headers']['BOOTPAY-ROLE'] == 'supervisor'

    # 청구서 목록 (확장 파라미터)
    with patch('requests.get', record):
        commerce.invoice.list({'page': 1, 'limit': 24, 'cs_type': 'CS_TYPE', 'user_id': 'USER_ID'})

    assert 'cs_type=CS_TYPE' in requested['url'], requested['url']
    assert 'user_id=USER_ID' in requested['url'], requested['url']

    # 청구서 재안내 (send_types 생략 가능)
    with patch('requests.post', record):
        commerce.invoice.notify('INVOICE_ID')

    assert requested['url'].endswith('/invoices/INVOICE_ID/notify'), requested['url']
    assert requested['json'] == {}

    # 주문 목록 (search_date_from/to 가 정식 키)
    with patch('requests.get', record):
        commerce.order.list({'page': 1, 'limit': 20, 'search_date_from': '2026-08-01',
                             'search_date_to': '2026-08-31'})

    assert 'search_date_from=2026-08-01' in requested['url'], requested['url']
    assert 'search_date_to=2026-08-31' in requested['url'], requested['url']

    # 주문 취소 승인 - order_cancellation_request_id 로 통일 (구 키도 지원)
    with patch('requests.put', record):
        commerce.order_cancel.approve({'order_cancellation_request_id': 'CANCEL_ID'})

    assert requested['url'].endswith('/order/cancel/CANCEL_ID/approve'), requested['url']

    with patch('requests.put', record):
        commerce.order_cancel.reject({'order_cancel_request_history_id': 'LEGACY_ID'})

    assert requested['url'].endswith('/order/cancel/LEGACY_ID/reject'), requested['url']

    # 이미지가 없으면 상품 생성은 JSON 으로 전송된다
    with patch('requests.post', record):
        commerce.product.create({'name': '테스트 상품', 'display_price': 10000})

    assert requested['url'].endswith('/products'), requested['url']
    assert requested['json'] == {'name': '테스트 상품', 'display_price': 10000}

    print('=== Commerce API 엔드포인트 테스트 통과 ===')


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
    test_commerce_endpoints()

    # 실제 API 테스트
    test_get_access_token()
    test_user_list()
    test_product_list()
    test_order_list()
    test_with_token_chaining()

    print('\n테스트 완료!')
