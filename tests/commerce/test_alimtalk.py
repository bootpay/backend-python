"""Commerce API - 알림톡(v1 /alimtalk) wire-format 테스트 (HTTP mock 기반, 네트워크 불필요).

⚠️ 알림톡 API 는 실제로 카카오톡이 발송되고 과금된다(샌드박스 없음) —
   라이브 호출 테스트를 두지 않고 요청 형태만 검증한다.
"""
import pytest

from bootpay_backend.commerce import BootpayCommerce


class _Response:
    def __init__(self, payload=None, text='', content_type='application/json', status_code=200):
        self._payload = payload if payload is not None else {'success': True}
        self.text = text
        self.headers = {'Content-Type': content_type}
        self.status_code = status_code

    def json(self):
        return self._payload


@pytest.fixture
def commerce():
    return BootpayCommerce(client_key='ck', secret_key='sk', mode='development')


@pytest.fixture
def captured(monkeypatch):
    """requests.* 호출을 가로채 마지막 요청의 method/url/헤더/바디를 기록한다."""
    box = {'response': _Response()}

    def _capture(method):
        def fake(url, headers=None, params=None, json=None, data=None, files=None, timeout=None):
            box.update(method=method, url=url, headers=headers or {},
                       params=params, json=json, data=data, files=files)
            return box['response']
        return fake

    monkeypatch.setattr('requests.get', _capture('get'))
    monkeypatch.setattr('requests.post', _capture('post'))
    monkeypatch.setattr('requests.put', _capture('put'))
    monkeypatch.setattr('requests.delete', _capture('delete'))
    return box


# ---------------------------------------------------------------------------
# 경로 · 동사 · scope — 35종 전수
# ---------------------------------------------------------------------------
ROUTES = [
    # (label, call, method, path)
    ('message.list', lambda c: c.alimtalk_message.list(), 'get', '/v1/alimtalk/messages'),
    ('message.stats', lambda c: c.alimtalk_message.stats(), 'get', '/v1/alimtalk/messages/stats'),
    ('message.detail', lambda c: c.alimtalk_message.detail('r1'), 'get', '/v1/alimtalk/messages/r1'),

    ('official.list', lambda c: c.alimtalk_official.list(), 'get', '/v1/alimtalk/official'),
    ('official.recommend', lambda c: c.alimtalk_official.recommend({'text': '주문이 접수되었습니다'}),
     'post', '/v1/alimtalk/official/recommend'),
    ('official.detail', lambda c: c.alimtalk_official.detail('BP001'), 'get', '/v1/alimtalk/official/BP001'),

    ('optout.list', lambda c: c.alimtalk_optout.list(), 'get', '/v1/alimtalk/optouts'),
    ('optout.create', lambda c: c.alimtalk_optout.create({'phone': '01012345678'}),
     'post', '/v1/alimtalk/optouts'),
    ('optout.check', lambda c: c.alimtalk_optout.check({'phone': '01012345678'}),
     'post', '/v1/alimtalk/optouts/check'),
    ('optout.release', lambda c: c.alimtalk_optout.release('01012345678'),
     'delete', '/v1/alimtalk/optouts/01012345678'),

    ('send.send', lambda c: c.alimtalk_send.send({'template_code': 'T1', 'to': '01012345678'}),
     'post', '/v1/alimtalk/send'),
    ('send.bulk', lambda c: c.alimtalk_send.bulk({'template_code': 'T1', 'recipients': []}),
     'post', '/v1/alimtalk/send/bulk'),
    ('send.cancel', lambda c: c.alimtalk_send.cancel('r1'), 'delete', '/v1/alimtalk/send/r1'),

    ('sender.categories', lambda c: c.alimtalk_sender.categories(), 'get', '/v1/alimtalk/categories'),
    ('sender.otp', lambda c: c.alimtalk_sender.otp({'yellow_id': '@bootpay', 'phone': '01012345678'}),
     'post', '/v1/alimtalk/senders/otp'),
    ('sender.create', lambda c: c.alimtalk_sender.create({'otp': '123456', 'yellow_id': '@bootpay',
                                                          'phone': '01012345678', 'category_code': '001'}),
     'post', '/v1/alimtalk/senders'),
    ('sender.list', lambda c: c.alimtalk_sender.list(), 'get', '/v1/alimtalk/senders'),
    ('sender.detail', lambda c: c.alimtalk_sender.detail('ksp1'), 'get', '/v1/alimtalk/senders/ksp1'),
    ('sender.release', lambda c: c.alimtalk_sender.release('ksp1'), 'delete', '/v1/alimtalk/senders/ksp1'),
    ('sender.variable_examples',
     lambda c: c.alimtalk_sender.variable_examples('ksp1', {'user_name': '홍길동'}),
     'put', '/v1/alimtalk/senders/ksp1/variable_examples'),

    ('template.list', lambda c: c.alimtalk_template.list(), 'get', '/v1/alimtalk/templates'),
    ('template.create', lambda c: c.alimtalk_template.create({'ksp_id': 'ksp1', 'name': 'T'}),
     'post', '/v1/alimtalk/templates'),
    ('template.detail', lambda c: c.alimtalk_template.detail('t1'), 'get', '/v1/alimtalk/templates/t1'),
    ('template.update', lambda c: c.alimtalk_template.update('t1', {'name': 'T'}),
     'put', '/v1/alimtalk/templates/t1'),
    ('template.delete', lambda c: c.alimtalk_template.delete('t1'), 'delete', '/v1/alimtalk/templates/t1'),
    ('template.register', lambda c: c.alimtalk_template.register('t1'),
     'post', '/v1/alimtalk/templates/t1/register'),
    ('template.inspect', lambda c: c.alimtalk_template.inspect('t1'),
     'post', '/v1/alimtalk/templates/t1/inspect'),

    ('webhook.detail', lambda c: c.alimtalk_webhook.detail(), 'get', '/v1/alimtalk/webhook'),
    ('webhook.update', lambda c: c.alimtalk_webhook.update({'url': 'https://x.com/hook'}),
     'put', '/v1/alimtalk/webhook'),
    ('webhook.test', lambda c: c.alimtalk_webhook.test(), 'post', '/v1/alimtalk/webhook/test'),
    ('webhook.rotate_secret', lambda c: c.alimtalk_webhook.rotate_secret(),
     'post', '/v1/alimtalk/webhook/secret'),
    ('webhook.deliveries', lambda c: c.alimtalk_webhook.deliveries(),
     'get', '/v1/alimtalk/webhook/deliveries'),
]


@pytest.mark.parametrize('label,call,method,path', ROUTES, ids=[r[0] for r in ROUTES])
def test_alimtalk_routes_and_verbs(commerce, captured, label, call, method, path):
    call(commerce)
    assert captured['method'] == method, label
    assert captured['url'].split('?')[0].endswith(path), label


@pytest.mark.parametrize('label,call,method,path', ROUTES, ids=[r[0] for r in ROUTES])
def test_alimtalk_always_sends_user_role_without_idempotency_key(commerce, captured, label, call, method, path):
    """알림톡 스코프 키는 전부 user:alimtalk_* 이고, 서버는 Idempotency-Key 를 읽지 않는다.

    붙이면 서버가 주지 않는 멱등 보장을 주는 것처럼 보인다 — 멱등은 발송의 ref_id 로만 성립한다.
    """
    commerce.as_supervisor()  # 세션 role 이 무엇이든 알림톡은 user 로 나가야 한다
    call(commerce)

    assert captured['headers']['BOOTPAY-ROLE'] == 'user', label
    assert 'Idempotency-Key' not in captured['headers'], label


# ---------------------------------------------------------------------------
# 발송 (send)
# ---------------------------------------------------------------------------
def test_send_keeps_explicit_false_fallback(commerce, captured):
    """⚠️ fallback 미지정(None)과 False 는 다르다 — None 은 프로젝트 기본값, False 는 명시적으로 끈다."""
    commerce.alimtalk_send.send({
        'template_code': 'T1',
        'to': '01012345678',
        'variables': {'user_name': '홍길동'},
        'ref_id': 'order-1',
        'fallback': False,
    })

    assert captured['json'] == {
        'template_code': 'T1',
        'to': '01012345678',
        'variables': {'user_name': '홍길동'},
        'ref_id': 'order-1',
        'fallback': False,
    }


def test_send_drops_none_but_keeps_zero_like_values(commerce, captured):
    commerce.alimtalk_send.send({
        'template_code': 'T1',
        'to': '01012345678',
        'fallback': None,
        'reserved_at': None,
        'sender_key': 'sk-public',
    })

    assert captured['json'] == {'template_code': 'T1', 'to': '01012345678', 'sender_key': 'sk-public'}


def test_send_bulk_sends_recipients_as_is(commerce, captured):
    recipients = [
        {'to': '01012345678', 'ref_id': 'bulk-0001', 'variables': {'user_name': '홍길동'}},
        {'to': '01087654321', 'ref_id': 'bulk-0002', 'variables': {'user_name': '김철수'}},
    ]
    commerce.alimtalk_send.bulk({'template_code': 'T1', 'recipients': recipients, 'fallback': True})

    assert captured['url'].endswith('/v1/alimtalk/send/bulk')
    assert captured['json']['recipients'] == recipients
    assert captured['json']['fallback'] is True


# ---------------------------------------------------------------------------
# 발송내역 (message)
# ---------------------------------------------------------------------------
def test_message_list_sends_filters_as_query(commerce, captured):
    commerce.alimtalk_message.list({
        'template_code': 'T1',
        'status': 'success',
        'ref_id': 'order-1',
        'to': '01012345678',
        's_at': '2026-08-01',
        'e_at': '2026-08-27',
        'page': 2,
        'limit': 50,
        'unknown': None,
    })

    url = captured['url']
    assert captured['method'] == 'get'
    for expected in ['template_code=T1', 'status=success', 'ref_id=order-1', 'page=2', 'limit=50',
                     's_at=2026-08-01', 'e_at=2026-08-27']:
        assert expected in url
    assert 'unknown=' not in url


def test_message_stats_without_params_sends_bare_path(commerce, captured):
    commerce.alimtalk_message.stats()
    assert captured['url'].endswith('/v1/alimtalk/messages/stats')
    assert '?' not in captured['url']


# ---------------------------------------------------------------------------
# 공식 템플릿 (official)
# ---------------------------------------------------------------------------
def test_official_list_maps_keyword_to_canonical_q(commerce, captured):
    """서버는 q 를 먼저 보고 없으면 keyword 를 본다 — 정본 키인 q 로 보낸다."""
    commerce.alimtalk_official.list({'keyword': '주문', 'msg_type': 'BA', 'per': 50, 'ksp_id': 'ksp1'})

    url = captured['url']
    assert 'q=%EC%A3%BC%EB%AC%B8' in url
    assert 'keyword=' not in url
    assert 'msg_type=BA' in url
    assert 'per=50' in url
    assert 'ksp_id=ksp1' in url


def test_official_recommend_sends_text_in_body(commerce, captured):
    commerce.alimtalk_official.recommend({'text': '주문이 접수되었습니다', 'limit': 3, 'category': None})

    assert captured['method'] == 'post'
    assert captured['json'] == {'text': '주문이 접수되었습니다', 'limit': 3}


def test_official_detail_supports_ksp_id_for_variable_examples(commerce, captured):
    commerce.alimtalk_official.detail('BP001', ksp_id='ksp1')
    assert captured['url'].endswith('/v1/alimtalk/official/BP001?ksp_id=ksp1')

    commerce.alimtalk_official.detail('BP001')
    assert captured['url'].endswith('/v1/alimtalk/official/BP001')


# ---------------------------------------------------------------------------
# 수신거부 (optout)
# ---------------------------------------------------------------------------
def test_optout_check_supports_single_and_bulk_phones(commerce, captured):
    commerce.alimtalk_optout.check({'phones': ['01012345678', '01087654321']})
    assert captured['json'] == {'phones': ['01012345678', '01087654321']}

    commerce.alimtalk_optout.check({'phone': '01012345678'})
    assert captured['json'] == {'phone': '01012345678'}


def test_optout_release_puts_phone_in_path(commerce, captured):
    commerce.alimtalk_optout.release('010-1234-5678')
    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/alimtalk/optouts/010-1234-5678')


# ---------------------------------------------------------------------------
# 발신프로필 (sender)
# ---------------------------------------------------------------------------
def test_sender_detail_serializes_sync_as_lowercase_bool(commerce, captured):
    """⚠️ urlencode 의 'True'/'False' 를 그대로 보내면 Rails 가 'False' 를 참으로 캐스팅한다."""
    commerce.alimtalk_sender.detail('ksp1', sync=True)
    assert captured['url'].endswith('/v1/alimtalk/senders/ksp1?sync=true')

    commerce.alimtalk_sender.detail('ksp1', sync=False)
    assert captured['url'].endswith('/v1/alimtalk/senders/ksp1?sync=false')

    commerce.alimtalk_sender.detail('ksp1')
    assert captured['url'].endswith('/v1/alimtalk/senders/ksp1')


def test_sender_variable_examples_wraps_payload_in_examples_key(commerce, captured):
    commerce.alimtalk_sender.variable_examples('ksp1', {'user_name': '홍길동', 'company_name': '부트페이몰'})

    assert captured['method'] == 'put'
    assert captured['json'] == {'examples': {'user_name': '홍길동', 'company_name': '부트페이몰'}}


# ---------------------------------------------------------------------------
# 자체 템플릿 (template)
# ---------------------------------------------------------------------------
def test_template_create_keeps_explicit_false_register(commerce, captured):
    """⚠️ register: False 를 떨구면 생성 즉시 대행사·카카오에 실제 등록된다."""
    commerce.alimtalk_template.create({
        'ksp_id': 'ksp1',
        'name': '주문완료',
        'content': '#{user_name}님 주문이 완료되었습니다.',
        'register': False,
        'buttons': None,
    })

    assert captured['json'] == {
        'ksp_id': 'ksp1',
        'name': '주문완료',
        'content': '#{user_name}님 주문이 완료되었습니다.',
        'register': False,
    }


def test_template_create_passes_through_unlisted_fields(commerce, captured):
    """서버가 읽는 필드가 늘어나도 SDK 수정 없이 전달된다 (ruby 의 **attrs 와 같은 계약)."""
    commerce.alimtalk_template.create({'ksp_id': 'ksp1', 'brand_new_field': 'v'})
    assert captured['json'] == {'ksp_id': 'ksp1', 'brand_new_field': 'v'}


def test_template_detail_supports_sync_false_for_drafts(commerce, captured):
    """⚠️ 서버 기본값이 sync=true 라 초안 조회에는 false 를 명시해야 한다."""
    commerce.alimtalk_template.detail('t1', sync=False)
    assert captured['url'].endswith('/v1/alimtalk/templates/t1?sync=false')


def test_template_list_sends_inspection_filters(commerce, captured):
    commerce.alimtalk_template.list({'ins': 3, 'sort': 'latest', 'keyword': 'order'})

    url = captured['url']
    assert 'ins=3' in url
    assert 'sort=latest' in url
    assert 'keyword=order' in url


def test_template_export_defaults_to_json_and_parses_body(commerce, captured):
    """서버 기본은 csv 지만 SDK 기본은 json 이다 — csv 본문은 공용 get 의 파싱을 통과하지 못한다."""
    captured['response'] = _Response(payload={'list': []})
    result = commerce.alimtalk_template.export({'scope': 'official'})

    assert captured['method'] == 'get'
    assert 'format=json' in captured['url']
    assert 'scope=official' in captured['url']
    assert result == {'list': []}


def test_template_export_csv_returns_raw_body_without_json_parsing(commerce, captured):
    """csv 를 response.json() 으로 파싱하면 성공한 요청이 통신 실패로 보고된다."""
    captured['response'] = _Response(text='code,name\nT1,주문완료\n', content_type='text/csv')
    result = commerce.alimtalk_template.export({'format': 'csv', 'include_content': True})

    assert captured['method'] == 'get'
    assert captured['url'].endswith('/v1/alimtalk/templates/export')
    assert captured['params'] == {'format': 'csv', 'include_content': 'true'}
    assert captured['headers']['Accept'] == '*/*'
    assert result == {
        'body': 'code,name\nT1,주문완료\n',
        'content_type': 'text/csv',
        'status': 200,
    }


def test_template_image_uploads_single_named_file_field(commerce, captured, tmp_path):
    """⚠️ 서버가 필드명을 image 로 정해 뒀다 — images[0] 으로 올리면 파일을 찾지 못한다."""
    image = tmp_path / 'banner.jpg'
    image.write_bytes(b'jpeg')

    commerce.alimtalk_template.image(str(image), replace_url='https://cdn/old.jpg')

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/alimtalk/templates/image')
    assert list(captured['files'].keys()) == ['image']
    assert captured['files']['image'][0] == 'banner.jpg'
    assert captured['data'] == {'replace_url': 'https://cdn/old.jpg'}
    # Content-Type 을 수동 지정하면 boundary 가 유실된다 — requests 에 맡긴다.
    assert 'Content-Type' not in captured['headers']
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'


def test_template_highlight_image_uses_its_own_endpoint(commerce, captured, tmp_path):
    """본문 이미지와 규격이 달라(1:1 · 108px) endpoint 가 분리돼 있다."""
    image = tmp_path / 'thumb.jpg'
    image.write_bytes(b'jpeg')

    commerce.alimtalk_template.highlight_image(str(image))

    assert captured['url'].endswith('/v1/alimtalk/templates/highlight_image')
    assert list(captured['files'].keys()) == ['image']
    assert captured['data'] == {}


def test_template_image_accepts_file_object(commerce, captured, tmp_path):
    image = tmp_path / 'banner.jpg'
    image.write_bytes(b'jpeg')

    with open(image, 'rb') as fp:
        commerce.alimtalk_template.image(fp)
        assert captured['files']['image'][1] is fp
    assert captured['files']['image'][0] == 'banner.jpg'


# ---------------------------------------------------------------------------
# 웹훅 (webhook) — 주문·구독 통합 웹훅과 별개 endpoint 다
# ---------------------------------------------------------------------------
def test_alimtalk_webhook_is_separate_from_order_webhook(commerce, captured):
    commerce.alimtalk_webhook.test()
    assert captured['url'].endswith('/v1/alimtalk/webhook/test')

    commerce.webhook.send_test()
    assert captured['url'].endswith('/v1/webhook/test')


def test_webhook_update_keeps_explicit_false_enabled(commerce, captured):
    """enabled: False 는 웹훅을 끄는 값이라 떨구면 안 된다."""
    commerce.alimtalk_webhook.update({
        'url': 'https://example.com/hook',
        'events': [301, 302],
        'enabled': False,
    })

    assert captured['method'] == 'put'
    assert captured['json'] == {
        'url': 'https://example.com/hook',
        'events': [301, 302],
        'enabled': False,
    }


def test_webhook_update_drops_none_values(commerce, captured):
    commerce.alimtalk_webhook.update({'url': 'https://example.com/hook', 'events': None, 'enabled': None})
    assert captured['json'] == {'url': 'https://example.com/hook'}


def test_webhook_deliveries_sends_pagination(commerce, captured):
    commerce.alimtalk_webhook.deliveries({'page': 2, 'limit': 100})

    url = captured['url']
    assert 'page=2' in url
    assert 'limit=100' in url


def test_webhook_event_code_constants():
    """events 에 실을 이벤트 코드는 상수로 노출한다 (목록에 없는 값은 서버가 조용히 버린다)."""
    from bootpay_backend.commerce import (
        ALIMTALK_WEBHOOK_EVENT_SEND_REQUESTED,
        ALIMTALK_WEBHOOK_EVENT_SEND_SUCCESS,
        ALIMTALK_WEBHOOK_EVENT_SEND_FAILED,
        ALIMTALK_WEBHOOK_EVENT_SEND_CANCELED,
        ALIMTALK_WEBHOOK_EVENT_FALLBACK_SENT,
        ALIMTALK_WEBHOOK_EVENT_TEMPLATE_APPROVED,
        ALIMTALK_WEBHOOK_EVENT_TEMPLATE_REJECTED,
        ALIMTALK_WEBHOOK_EVENT_OPTOUT_CREATED,
    )

    assert [
        ALIMTALK_WEBHOOK_EVENT_SEND_REQUESTED,
        ALIMTALK_WEBHOOK_EVENT_SEND_SUCCESS,
        ALIMTALK_WEBHOOK_EVENT_SEND_FAILED,
        ALIMTALK_WEBHOOK_EVENT_SEND_CANCELED,
        ALIMTALK_WEBHOOK_EVENT_FALLBACK_SENT,
        ALIMTALK_WEBHOOK_EVENT_TEMPLATE_APPROVED,
        ALIMTALK_WEBHOOK_EVENT_TEMPLATE_REJECTED,
        ALIMTALK_WEBHOOK_EVENT_OPTOUT_CREATED,
    ] == [300, 301, 302, 303, 304, 310, 311, 320]
