"""Commerce API - NodeJS 2.9.0 parity wire-format tests (HTTP mock 기반, 네트워크 불필요)."""
import pytest

from bootpay_backend.commerce import BootpayCommerce


class _Response:
    def __init__(self, payload=None):
        self._payload = payload if payload is not None else {'success': True}

    def json(self):
        return self._payload


@pytest.fixture
def commerce():
    return BootpayCommerce(client_key='ck', secret_key='sk', mode='development')


@pytest.fixture
def captured(monkeypatch):
    """requests.* 호출을 가로채 마지막 요청의 method/url/헤더/바디를 기록한다."""
    box = {}

    def _capture(method):
        def fake(url, headers=None, params=None, json=None, data=None, files=None, timeout=None):
            box.update(method=method, url=url, headers=headers or {},
                       params=params, json=json, data=data, files=files)
            return _Response()
        return fake

    monkeypatch.setattr('requests.get', _capture('get'))
    monkeypatch.setattr('requests.post', _capture('post'))
    monkeypatch.setattr('requests.put', _capture('put'))
    monkeypatch.setattr('requests.delete', _capture('delete'))
    return box


# ---------------------------------------------------------------------------
# BOOTPAY-ROLE / Idempotency-Key 헤더
# ---------------------------------------------------------------------------
def test_request_level_role_is_not_overwritten_by_common_layer(commerce, captured):
    """요청별로 지정된 supervisor role 을 공통 계층이 user 로 덮어쓰면 안 된다."""
    assert commerce.get_role() == 'user'
    commerce.mall_setting.get_mall_setting()

    assert captured['method'] == 'get'
    assert captured['url'].endswith('/v1/mall-setting')
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'
    assert captured['headers']['Idempotency-Key']


def test_idempotency_key_can_be_passed_explicitly(commerce, captured):
    commerce.mall_setting.get_mall_setting(idempotency_key='fixed-key')
    assert captured['headers']['Idempotency-Key'] == 'fixed-key'


def test_store_get_attaches_idempotency_key(commerce, captured):
    commerce.store.get_store()
    assert captured['url'].endswith('/v1/store')
    assert captured['headers']['Idempotency-Key']

    commerce.store.get_store_detail(idempotency_key='store-key')
    assert captured['url'].endswith('/v1/store/detail')
    assert captured['headers']['Idempotency-Key'] == 'store-key'


# ---------------------------------------------------------------------------
# mallSetting / webhook
# ---------------------------------------------------------------------------
def test_mall_setting_update_drops_none_values(commerce, captured):
    commerce.mall_setting.update_mall_setting({'name': '테스트몰', 'description': None})

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/mall-setting')
    assert captured['json'] == {'name': '테스트몰'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_mall_setting_aliases_hit_same_endpoints(commerce, captured):
    commerce.mall_setting.detail()
    assert captured['method'] == 'get'
    assert captured['url'].endswith('/v1/mall-setting')

    commerce.mall_setting.update({'name': '별칭'})
    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/mall-setting')
    assert captured['json'] == {'name': '별칭'}


def test_webhook_send_test_body_and_header(commerce, captured):
    commerce.webhook.send_test()
    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/webhook/test')
    assert captured['json'] == {}
    assert captured['headers']['Idempotency-Key']

    commerce.webhook.send_test({'header_content_type': 1, 'idempotency_key': 'wh-key'})
    assert captured['json'] == {'header_content_type': 1}
    assert captured['headers']['Idempotency-Key'] == 'wh-key'


# ---------------------------------------------------------------------------
# supervisorCharge — charge_key 는 body 로만 전송
# ---------------------------------------------------------------------------
def test_supervisor_charge_sends_charge_key_in_body_only(commerce, captured):
    commerce.order_subscription.supervisor_charge({
        'charge_key': 'SECRET_CHARGE_KEY',
        'price': 1000,
        'tax_free_price': 0,
    })

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/order_subscriptions/charge')
    assert 'SECRET_CHARGE_KEY' not in captured['url']
    assert captured['json']['charge_key'] == 'SECRET_CHARGE_KEY'
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'
    assert captured['headers']['Idempotency-Key']


def test_supervisor_charge_revoke_uses_delete_with_body(commerce, captured):
    commerce.order_subscription.supervisor_charge_revoke({
        'charge_key': 'SECRET_CHARGE_KEY',
        'idempotency_key': 'revoke-key',
    })

    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/order_subscriptions/charge')
    assert 'SECRET_CHARGE_KEY' not in captured['url']
    assert captured['json'] == {'charge_key': 'SECRET_CHARGE_KEY'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'
    assert captured['headers']['Idempotency-Key'] == 'revoke-key'


# ---------------------------------------------------------------------------
# requestIng — purchase / transfer
# ---------------------------------------------------------------------------
def test_request_ing_purchase_and_transfer_routes(commerce, captured):
    commerce.order_subscription.request_ing.purchase({'order_subscription_id': 'os1', 'price': 1000})
    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/order_subscriptions/requests/ing/purchase')
    assert captured['json'] == {'order_subscription_id': 'os1', 'price': 1000}
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'

    commerce.order_subscription.request_ing.transfer({'order_subscription_id': 'os1', 'new_user_id': 'u2'})
    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/order_subscriptions/requests/ing/transfer')
    assert captured['json'] == {'order_subscription_id': 'os1', 'new_user_id': 'u2'}


def test_request_ing_resume_stays_put(commerce, captured):
    """requests/ing 계열 중 유일하게 PUT 이다."""
    commerce.order_subscription.request_ing.resume({'order_subscription_id': 'os1'})
    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/order_subscriptions/requests/ing/resume')


def test_request_ing_idempotency_key_moves_to_header_not_body(commerce, captured):
    """idempotency_key 는 Idempotency-Key 헤더로만 나가고 body 에는 포함되지 않는다. None 값도 미전송."""
    commerce.order_subscription.request_ing.pause({
        'order_subscription_id': 'os1',
        'reason': None,
        'idempotency_key': 'pause-key',
    })
    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/order_subscriptions/requests/ing/pause')
    assert captured['json'] == {'order_subscription_id': 'os1'}
    assert captured['headers']['Idempotency-Key'] == 'pause-key'
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'

    commerce.order_subscription.request_ing.termination({
        'order_subscription_id': 'os1',
        'idempotency_key': 'term-key',
    })
    assert captured['url'].endswith('/v1/order_subscriptions/requests/ing/termination')
    assert captured['json'] == {'order_subscription_id': 'os1'}
    assert captured['headers']['Idempotency-Key'] == 'term-key'


# ---------------------------------------------------------------------------
# Mall 회원 (users/...)
# ---------------------------------------------------------------------------
def test_user_login_uses_plural_users_route_and_default_corporate_type(commerce, captured):
    commerce.user.user_login({'login_id': 'tester', 'password': 'pw'})

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/users/login')
    assert captured['json'] == {'login_id': 'tester', 'password': 'pw', 'corporate_type': 0}
    assert 'Bootpay-User-JWT' not in captured['headers']


def test_user_session_attaches_jwt_header_only_when_present(commerce, captured):
    commerce.user.user_session()
    assert captured['method'] == 'get'
    assert captured['url'].endswith('/v1/users/session')
    assert 'Bootpay-User-JWT' not in captured['headers']

    commerce.user.user_session(user_jwt='member-jwt')
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'


def test_user_logout_uses_delete_session(commerce, captured):
    commerce.user.user_logout('member-jwt')
    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/users/session')
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'


def test_user_join_uses_plural_route_default_corporate_type_and_drops_none(commerce, captured):
    commerce.user.user_join({
        'login_id': 'newbie',
        'password': 'pw',
        'name': '가입자',
        'email': None,
        'idempotency_key': 'join-key',
    })

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/users/join')
    assert captured['json'] == {'login_id': 'newbie', 'password': 'pw', 'name': '가입자', 'corporate_type': 0}
    assert captured['headers']['Idempotency-Key'] == 'join-key'
    assert 'Bootpay-User-JWT' not in captured['headers']


def test_user_join_check_and_uid_exist_routes(commerce, captured):
    commerce.user.user_join_check('email-exist', 'a@b.com')
    assert captured['url'].endswith('/v1/users/join/email-exist?pk=a%40b.com')

    commerce.user.uid_exist('uid 123')
    assert captured['url'].endswith('/v1/users/join/uid-exist?pk=uid%20123')
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'


# ---------------------------------------------------------------------------
# Mall 상품
# ---------------------------------------------------------------------------
def test_products_mall_defaults_page_1_limit_20(commerce, captured):
    commerce.product.products()
    assert captured['method'] == 'get'
    assert 'page=1' in captured['url'] and 'limit=20' in captured['url']
    assert 'Idempotency-Key' in captured['headers']

    commerce.product.products({'category_id': 'cat1', 'user_jwt': 'member-jwt'})
    assert 'category_id=cat1' in captured['url']
    assert 'user_jwt' not in captured['url']
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'


def test_product_detail_mall_supports_jwt(commerce, captured):
    commerce.product.product_detail('prod1', user_jwt='member-jwt')
    assert captured['url'].endswith('/v1/products/prod1')
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'


def test_product_create_without_images_sends_json(commerce, captured):
    commerce.product.create({'name': '테스트 상품', 'price': 1000, 'memo': None})
    assert captured['method'] == 'post'
    assert captured['json'] == {'name': '테스트 상품', 'price': 1000}
    assert captured['files'] is None
    assert captured['headers']['BOOTPAY-ROLE'] == 'manager'


def test_product_create_with_images_uses_indexed_multipart(commerce, captured, tmp_path):
    """Rails 는 반복 `images` 를 배열로 안 받는다 — images[0], images[1] 인덱싱 필수."""
    image1 = tmp_path / 'a.jpg'
    image2 = tmp_path / 'b.jpg'
    image1.write_bytes(b'a')
    image2.write_bytes(b'b')

    commerce.product.create({'name': '테스트 상품'}, [str(image1), str(image2)])

    assert captured['method'] == 'post'
    field_names = [field for field, _ in captured['files']]
    assert field_names == ['images[0]', 'images[1]']
    assert captured['data'] == {'name': '테스트 상품'}
    # Content-Type 을 수동 지정하면 boundary 가 유실된다 — requests 에 맡긴다.
    assert 'Content-Type' not in captured['headers']
    assert captured['headers']['BOOTPAY-ROLE'] == 'manager'


# ---------------------------------------------------------------------------
# invoice
# ---------------------------------------------------------------------------
def test_product_status_uses_manager_role_and_strips_meta_keys(commerce, captured):
    commerce.product.status({'product_id': 'prod1', 'status_sale': False, 'idempotency_key': 'st-key'})

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/products/prod1/status')
    assert captured['json'] == {'status_sale': False}
    assert captured['headers']['BOOTPAY-ROLE'] == 'manager'
    assert captured['headers']['Idempotency-Key'] == 'st-key'


def test_product_delete_uses_manager_role(commerce, captured):
    commerce.product.delete('prod1')
    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/products/prod1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'manager'
    assert captured['headers']['Idempotency-Key']


def test_invoice_list_defaults_and_new_params(commerce, captured):
    commerce.invoice.list()
    assert 'page=1' in captured['url'] and 'limit=24' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'

    commerce.invoice.list({'cs_type': 'paid', 'user_id': 'u1', 'product_type': 2,
                           'css_at': '2024-01-01', 'cse_at': '2024-12-31'})
    for fragment in ('cs_type=paid', 'user_id=u1', 'product_type=2', 'css_at=2024-01-01', 'cse_at=2024-12-31'):
        assert fragment in captured['url']


def test_invoice_notify_send_types_is_optional(commerce, captured):
    commerce.invoice.notify('inv1')
    assert captured['url'].endswith('/v1/invoices/inv1/notify')
    assert captured['json'] == {}

    commerce.invoice.notify('inv1', [1, 2])
    assert captured['json'] == {'send_types': [1, 2]}


# ---------------------------------------------------------------------------
# orderCancel — 인자명 통일 + 하위호환
# ---------------------------------------------------------------------------
def test_order_cancel_approve_accepts_new_and_legacy_id_names(commerce, captured):
    commerce.order_cancel.approve({'order_cancellation_request_id': 'ocr1', 'message': '승인'})
    assert captured['url'].endswith('/v1/order/cancel/ocr1/approve')
    assert captured['json'] == {'message': '승인'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'

    commerce.order_cancel.reject({'order_cancel_request_history_id': 'ocr2', 'message': '반려'})
    assert captured['url'].endswith('/v1/order/cancel/ocr2/reject')
    assert captured['json'] == {'message': '반려'}


def test_order_cancel_both_actions_accept_both_id_names(commerce, captured):
    """approve/reject 각각 신·구 인자명 양쪽 모두 동작해야 한다 (교차 검증)."""
    commerce.order_cancel.approve({'order_cancel_request_history_id': 'ocr-legacy', 'message': '승인'})
    assert captured['url'].endswith('/v1/order/cancel/ocr-legacy/approve')

    commerce.order_cancel.reject({'order_cancellation_request_id': 'ocr-new', 'message': '반려'})
    assert captured['url'].endswith('/v1/order/cancel/ocr-new/reject')


def test_order_cancel_approve_requires_id(commerce, captured):
    with pytest.raises(ValueError):
        commerce.order_cancel.approve({'message': '승인'})


def test_order_cancel_withdraw_accepts_string_dict_and_legacy_kwarg(commerce, captured):
    commerce.order_cancel.withdraw('ocr1')
    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/order/cancel/ocr1/withdraw')
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'

    commerce.order_cancel.withdraw({'order_cancellation_request_id': 'ocr2'})
    assert captured['url'].endswith('/v1/order/cancel/ocr2/withdraw')

    commerce.order_cancel.withdraw(order_cancel_request_history_id='ocr3')
    assert captured['url'].endswith('/v1/order/cancel/ocr3/withdraw')


# ---------------------------------------------------------------------------
# adjustment — delete body / update adjustments 배열
# ---------------------------------------------------------------------------
def test_adjustment_delete_sends_target_id_in_body(commerce, captured):
    commerce.order_subscription_adjustment.delete('os1', 'adj1')

    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/order_subscriptions/os1/adjustments')
    assert '?' not in captured['url']
    assert captured['json'] == {'order_subscription_adjustment_id': 'adj1'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_adjustment_update_supports_adjustments_array(commerce, captured):
    commerce.order_subscription_adjustment.update({
        'order_subscription_id': 'os1',
        'duration': 2,
        'adjustments': [{'price': -1000, 'name': '기간할인'}],
    })

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/order_subscriptions/os1/adjustments')
    assert captured['json'] == {'duration': 2, 'adjustments': [{'price': -1000, 'name': '기간할인'}]}


def test_adjustment_create_defaults(commerce, captured):
    commerce.order_subscription_adjustment.create('os1', {'name': '설치비', 'price': 5000})
    assert captured['json'] == {'price': 5000, 'duration': 1, 'tax_free_price': 0, 'name': '설치비'}


def test_adjustment_create_supports_duration_range(commerce, captured):
    """duration_from ~ duration_to 로 회차 범위를 지정한다 (3~7회차 각각 한 건씩)."""
    commerce.order_subscription_adjustment.create('os1', {
        'name': '기간할인',
        'price': -1000,
        'duration_from': 3,
        'duration_to': 7,
    })

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/order_subscriptions/os1/adjustments')
    assert captured['json'] == {
        'name': '기간할인', 'price': -1000, 'duration': 1, 'tax_free_price': 0,
        'duration_from': 3, 'duration_to': 7,
    }
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_adjustment_create_supports_unlimited_range(commerce, captured):
    """duration_from + is_unlimited 이면 해당 회차부터 계약 끝까지 (duration_to 는 무시된다)."""
    commerce.order_subscription_adjustment.create('os1', {
        'name': '무기한할인',
        'price': -500,
        'duration_from': 3,
        'is_unlimited': True,
        'duration_to': None,
    }, idempotency_key='adj-key')

    assert captured['json'] == {
        'name': '무기한할인', 'price': -500, 'duration': 1, 'tax_free_price': 0,
        'duration_from': 3, 'is_unlimited': True,
    }
    assert captured['headers']['Idempotency-Key'] == 'adj-key'


def test_adjustment_create_keeps_false_is_unlimited(commerce, captured):
    """None 만 제거한다 — is_unlimited=False 는 그대로 전송되어야 한다."""
    commerce.order_subscription_adjustment.create('os1', {
        'name': '단일회차',
        'price': 1000,
        'duration_from': 2,
        'duration_to': 4,
        'is_unlimited': False,
    })

    assert captured['json']['is_unlimited'] is False


# ---------------------------------------------------------------------------
# 파라미터 확장 — userGroup.limit / order.list / orderSubscription.list / orderSubscriptionRequest.list
# ---------------------------------------------------------------------------
def test_user_group_limit_uses_manager_role_and_new_params(commerce, captured):
    commerce.user_group.limit({
        'user_group_id': 'ug1',
        'use_limit': True,
        'limit_month_purchase': 100000,
        'limit_week_purchase': 50000,
    })

    assert captured['url'].endswith('/v1/user-groups/ug1/limit')
    assert captured['json'] == {'use_limit': True, 'limit_month_purchase': 100000, 'limit_week_purchase': 50000}
    assert captured['headers']['BOOTPAY-ROLE'] == 'manager'


def test_user_group_aggregate_transaction_uses_manager_role(commerce, captured):
    commerce.user_group.aggregate_transaction({
        'user_group_id': 'ug1',
        'use_subscription_aggregate_transaction': True,
        'subscription_month_day': 1,
    })

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/user-groups/ug1/aggregate-transaction')
    assert captured['json'] == {'use_subscription_aggregate_transaction': True, 'subscription_month_day': 1}
    assert captured['headers']['BOOTPAY-ROLE'] == 'manager'
    assert captured['headers']['Idempotency-Key']


def test_order_list_supports_search_date_range(commerce, captured):
    commerce.order.list({'search_date_from': '2024-01-01', 'search_date_to': '2024-12-31'})
    assert 'search_date_from=2024-01-01' in captured['url']
    assert 'search_date_to=2024-12-31' in captured['url']


def test_order_subscription_list_supports_search_date_and_status(commerce, captured):
    commerce.order_subscription.list({
        'search_date_from': '2024-01-01',
        'search_date_to': '2024-12-31',
        'status': 1,
    })
    assert 'search_date_from=2024-01-01' in captured['url']
    assert 'search_date_to=2024-12-31' in captured['url']
    assert 'status=1' in captured['url']


def test_order_subscription_bill_list_defaults_and_headers(commerce, captured):
    """bill.list — page/limit 기본 1/20 상시 전송 + Idempotency-Key + user role. 경로는 언더스코어."""
    commerce.order_subscription_bill.list()
    assert captured['method'] == 'get'
    assert '/v1/order_subscription_bills?' in captured['url']
    assert 'page=1' in captured['url'] and 'limit=20' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'
    assert captured['headers']['Idempotency-Key']

    commerce.order_subscription_bill.list({
        'order_subscription_id': 'os1',
        'status': [1, 2],
        'idempotency_key': 'bill-key',
    })
    assert 'order_subscription_id=os1' in captured['url']
    assert 'status=1%2C2' in captured['url']
    assert 'idempotency_key' not in captured['url']
    assert captured['headers']['Idempotency-Key'] == 'bill-key'


def test_calculate_termination_fee_sends_both_params_together(commerce, captured):
    """order_subscription_id 와 order_number 를 동시에 주면 둘 다 query 로 전송된다 (nodejs 와 동일)."""
    commerce.order_subscription.request_ing.calculate_termination_fee(
        order_subscription_id='os1',
        order_number='ON-1',
    )
    assert captured['method'] == 'get'
    assert 'order_subscription_id=os1' in captured['url']
    assert 'order_number=ON-1' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'
    assert captured['headers']['Idempotency-Key']


def test_order_subscription_request_detail_role_depends_on_project_id(commerce, captured):
    commerce.order_subscription_request.detail('req1')
    assert captured['url'].endswith('/v1/order-subscription-requests/req1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'

    commerce.order_subscription_request.detail('req1', project_id='proj1')
    assert captured['url'].endswith('/v1/order-subscription-requests/req1?project_id=proj1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_multipart_serializes_bool_as_lowercase(commerce, captured, tmp_path):
    """bool 은 소문자 'true'/'false' 로 전송 — str(False)='False' 는 Rails 가 true 로 캐스팅하는 실위험."""
    image = tmp_path / 'a.jpg'
    image.write_bytes(b'a')

    commerce.product.create(
        {'name': '상품', 'status_sale': False, 'use_stock': True, 'stock': 3},
        [str(image)],
    )

    assert captured['data'] == {'name': '상품', 'status_sale': 'false', 'use_stock': 'true', 'stock': '3'}


def test_order_subscription_update_uses_supervisor_role(commerce, captured):
    commerce.order_subscription.update({'order_subscription_id': 'os1', 'order_name': '변경'})
    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/order_subscriptions/os1')
    assert captured['json'] == {'order_name': '변경'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_order_subscription_update_sends_price(commerce, captured):
    """price 는 회차별 결제 기준금액 — 계약변경 body 로 그대로 전송된다."""
    commerce.order_subscription.update({
        'order_subscription_id': 'os1',
        'price': 15000,
        'order_name': None,
        'idempotency_key': 'price-key',
    })

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/order_subscriptions/os1')
    assert captured['json'] == {'price': 15000}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'
    assert captured['headers']['Idempotency-Key'] == 'price-key'


def test_order_subscription_request_list_role_depends_on_project_id(commerce, captured):
    commerce.order_subscription_request.list()
    assert 'page=1' in captured['url'] and 'limit=20' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'

    commerce.order_subscription_request.list({
        'project_id': 'proj1',
        'order_subscription_id': 'os1',
        'user_id': 'u1',
        'user_group_id': 'ug1',
    })
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'
    for fragment in ('project_id=proj1', 'order_subscription_id=os1', 'user_id=u1', 'user_group_id=ug1'):
        assert fragment in captured['url']


# ---------------------------------------------------------------------------
# scope(BOOTPAY-ROLE) 정합성 — 서버가 supervisor/manager 를 요구하는 엔드포인트
# 헤더를 붙이지 않으면 인스턴스 기본값 user 로 조용히 나가고 서버가 scope_invalid! 로 거절한다.
# ---------------------------------------------------------------------------
SCOPE_CASES = [
    ('supervisor_approve', lambda c: c.order_subscription.supervisor_approve('s1', {'reason': '승인'}),
     'put', '/v1/order_subscriptions/s1/approve', 'supervisor'),
    ('supervisor_reject', lambda c: c.order_subscription.supervisor_reject('s1', {'reason': '반려'}),
     'put', '/v1/order_subscriptions/s1/reject', 'supervisor'),
    ('supervisor_terminate', lambda c: c.order_subscription.supervisor_terminate('s1', {'reason': '해지'}),
     'put', '/v1/order_subscriptions/s1/terminate', 'supervisor'),
    ('supervisor_pause', lambda c: c.order_subscription.supervisor_pause('s1', {'paused_at': '2026-01-01'}),
     'put', '/v1/order_subscriptions/s1/pause', 'supervisor'),
    ('supervisor_resume', lambda c: c.order_subscription.supervisor_resume('s1'),
     'put', '/v1/order_subscriptions/s1/resume', 'supervisor'),
    ('category_create', lambda c: c.category.create({'name': '카테고리'}),
     'post', '/v1/categories', 'supervisor'),
    ('category_update', lambda c: c.category.update({'category_id': 'c1', 'name': '변경'}),
     'put', '/v1/categories/c1', 'supervisor'),
    ('category_destroy', lambda c: c.category.destroy('c1'),
     'delete', '/v1/categories/c1', 'supervisor'),
    ('user_group_user_create', lambda c: c.user_group.user_create('g1', 'u1'),
     'post', '/v1/user-groups/g1/user', 'manager'),
    ('user_group_user_delete', lambda c: c.user_group.user_delete('g1', 'u1'),
     'delete', '/v1/user-groups/g1/user/u1', 'manager'),
]


@pytest.mark.parametrize('label, call, method, path, role', SCOPE_CASES,
                         ids=[case[0] for case in SCOPE_CASES])
def test_scope_required_endpoints_send_expected_role(commerce, captured, label, call, method, path, role):
    call(commerce)

    assert captured['method'] == method, label
    assert captured['url'].endswith(path), label
    assert captured['headers']['BOOTPAY-ROLE'] == role, label
    assert captured['headers']['Idempotency-Key'], label


def test_explicit_idempotency_key_is_forwarded_and_kept_out_of_body(commerce, captured):
    commerce.category.create({'name': '카테고리', 'idempotency_key': 'fixed-key'})

    assert captured['headers']['Idempotency-Key'] == 'fixed-key'
    assert captured['json'] == {'name': '카테고리'}


# ---------------------------------------------------------------------------
# ruby SDK 누락 파라미터 반영 — orders / order_subscriptions / products / users
# ---------------------------------------------------------------------------
def test_order_list_supports_subscription_filters(commerce, captured):
    """구독 계약별·결제유형별 필터 — order_subscription_ids 는 콤마로 join 해서 보낸다."""
    commerce.order.list({
        'order_subscription_ids': ['os1', 'os2'],
        'subscription_billing_type': 1,
    })

    assert captured['method'] == 'get'
    assert 'order_subscription_ids=os1%2Cos2' in captured['url']
    assert 'subscription_billing_type=1' in captured['url']


def test_order_list_omits_empty_status_filters(commerce, captured):
    """값이 비었으면 status=&payment_status= 를 실어 보내지 않는다 (서버는 무시하지만 노이즈)."""
    commerce.order.list({'page': 1, 'status': [], 'payment_status': [], 'order_subscription_ids': []})

    assert 'status=' not in captured['url']
    assert 'payment_status=' not in captured['url']
    assert 'order_subscription_ids=' not in captured['url']


def test_order_subscription_list_supports_order_number(commerce, captured):
    """주문번호로 구독을 역조회한다."""
    commerce.order_subscription.list({'order_number': 'ON-1'})

    assert captured['method'] == 'get'
    assert '/v1/order_subscriptions?' in captured['url']
    assert 'order_number=ON-1' in captured['url']


def test_order_subscription_update_sends_memo(commerce, captured):
    """memo 는 변경이력에 남길 사유로 body 에 그대로 전송된다."""
    commerce.order_subscription.update({
        'order_subscription_id': 'os1',
        'price': 15000,
        'memo': '고객 요청으로 금액 변경',
    })

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/order_subscriptions/os1')
    assert captured['json'] == {'price': 15000, 'memo': '고객 요청으로 금액 변경'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_products_mall_supports_ex_uid(commerce, captured):
    """외부 UID 로 상품 조회 — 서버(v1/products_controller#index)가 params[:ex_uid] 를 읽는다."""
    commerce.product.products({'ex_uid': 'EX-1'})

    assert captured['method'] == 'get'
    assert 'ex_uid=EX-1' in captured['url']


def test_lookup_product_supports_jwt(commerce, captured):
    """lookup_product 도 product_detail 과 같이 회원 컨텍스트 조회를 지원한다."""
    commerce.product.lookup_product('prod1')
    assert captured['url'].endswith('/v1/products/prod1')
    assert 'Bootpay-User-JWT' not in captured['headers']

    commerce.product.lookup_product('prod1', user_jwt='member-jwt', idempotency_key='lp-key')
    assert captured['url'].endswith('/v1/products/prod1')
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'
    assert captured['headers']['Idempotency-Key'] == 'lp-key'


def test_user_list_sends_membership_type_not_member_type(commerce, captured):
    """서버가 읽는 회원등급 키는 membership_type 이다 — member_type 으로 보내면 조용히 무시된다."""
    commerce.user.list({'membership_type': 1})

    assert captured['method'] == 'get'
    assert 'membership_type=1' in captured['url']
    assert 'member_type=1' not in captured['url']


def test_user_list_maps_legacy_member_type_alias(commerce, captured):
    """기존 호출 호환 — member_type 은 membership_type 으로 매핑해서 보낸다."""
    commerce.user.list({'member_type': 2, 'keyword': '테스트'})

    assert 'membership_type=2' in captured['url']
    assert 'member_type=2' not in captured['url']

    # 둘 다 주면 정식 키가 우선한다.
    commerce.user.list({'membership_type': 1, 'member_type': 2})
    assert 'membership_type=1' in captured['url']
