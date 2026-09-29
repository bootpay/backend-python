"""Commerce API - 게시판(FAQ·공지사항·1:1문의·상품문의·상품평) wire-format 테스트 (HTTP mock 기반, 네트워크 불필요)."""
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
# FAQ (/v1/faqs)
# ---------------------------------------------------------------------------
def test_faq_list_defaults_to_user_role(commerce, captured):
    commerce.faq.list()

    assert captured['method'] == 'get'
    assert '/v1/faqs?' in captured['url']
    assert 'page=1' in captured['url']
    assert 'limit=20' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'
    assert captured['headers']['Idempotency-Key']


def test_faq_list_supervisor_can_request_all(commerce, captured):
    """supervisor 모드는 view=all 로 비공개 FAQ 까지 조회한다."""
    commerce.faq.list(page=2, limit=5, keyword='배송', view='all', supervisor=True, idempotency_key='faq-key')

    assert 'page=2' in captured['url']
    assert 'limit=5' in captured['url']
    assert 'view=all' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'
    assert captured['headers']['Idempotency-Key'] == 'faq-key'


def test_faq_detail_uses_role_header(commerce, captured):
    commerce.faq.detail('faq1', supervisor=True)

    assert captured['method'] == 'get'
    assert captured['url'].endswith('/v1/faqs/faq1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_faq_create_is_supervisor_only_and_drops_none(commerce, captured):
    commerce.faq.create(title='배송 문의', content='2~3일 걸립니다.', is_display=False)

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/faqs')
    assert captured['json'] == {'title': '배송 문의', 'content': '2~3일 걸립니다.', 'is_display': False}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_faq_update_sends_only_given_fields(commerce, captured):
    """images 는 보내면 목록 전체를 교체한다 — [] 도 그대로 실어야 한다."""
    commerce.faq.update('faq1', content='수정된 답변', images=[])

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/faqs/faq1')
    assert captured['json'] == {'content': '수정된 답변', 'images': []}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_faq_delete(commerce, captured):
    commerce.faq.delete('faq1')

    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/faqs/faq1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_faq_ruby_aliases_hit_same_endpoints(commerce, captured):
    commerce.faq.faqs()
    assert '/v1/faqs?' in captured['url']

    commerce.faq.faq_detail('faq1')
    assert captured['url'].endswith('/v1/faqs/faq1')

    commerce.faq.faq_create(title='t', content='c')
    assert captured['method'] == 'post'

    commerce.faq.faq_update('faq1', title='t')
    assert captured['method'] == 'put'

    commerce.faq.faq_delete('faq1')
    assert captured['method'] == 'delete'


# ---------------------------------------------------------------------------
# 공지사항 (/v1/notices)
# ---------------------------------------------------------------------------
def test_notice_list(commerce, captured):
    commerce.notice.list(keyword='점검', view='all', supervisor=True)

    assert captured['method'] == 'get'
    assert '/v1/notices?' in captured['url']
    assert 'view=all' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_notice_detail(commerce, captured):
    commerce.notice.detail('n1')

    assert captured['url'].endswith('/v1/notices/n1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'


def test_notice_create_sends_is_notice(commerce, captured):
    commerce.notice.create(title='서버 점검', content='0시부터', is_notice=True, is_display=True)

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/notices')
    assert captured['json'] == {
        'title': '서버 점검',
        'content': '0시부터',
        'is_notice': True,
        'is_display': True
    }
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_notice_update_and_delete(commerce, captured):
    commerce.notice.update('n1', is_display=False)
    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/notices/n1')
    assert captured['json'] == {'is_display': False}

    commerce.notice.delete('n1')
    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/notices/n1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_notice_ruby_aliases_hit_same_endpoints(commerce, captured):
    commerce.notice.notices()
    assert '/v1/notices?' in captured['url']

    commerce.notice.notice_detail('n1')
    assert captured['url'].endswith('/v1/notices/n1')

    commerce.notice.notice_create(title='t', content='c')
    assert captured['method'] == 'post'

    commerce.notice.notice_update('n1', title='t')
    assert captured['method'] == 'put'

    commerce.notice.notice_delete('n1')
    assert captured['method'] == 'delete'


# ---------------------------------------------------------------------------
# 1:1 문의 (/v1/inquiries)
# ---------------------------------------------------------------------------
def test_inquiry_list_sends_answered_as_lowercase_string(commerce, captured):
    """⚠️ answered 는 'true'/'false' 여야 한다 — 'False' 는 Rails 가 true 로 읽는다."""
    commerce.inquiry.list(answered=False, login_id='member01')

    assert captured['method'] == 'get'
    assert 'answered=false' in captured['url']
    assert 'login_id=member01' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'

    commerce.inquiry.list(answered=True)
    assert 'answered=true' in captured['url']

    commerce.inquiry.list()
    assert 'answered=' not in captured['url']


def test_inquiry_list_supervisor_attaches_jwt_header(commerce, captured):
    commerce.inquiry.list(user_id='u1', user_jwt='member-jwt', supervisor=True)

    assert 'user_id=u1' in captured['url']
    assert 'user_jwt' not in captured['url']
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_inquiry_detail_sends_member_query(commerce, captured):
    commerce.inquiry.detail('i1', login_id='member01')

    assert captured['url'].endswith('/v1/inquiries/i1?login_id=member01')

    commerce.inquiry.detail('i1')
    assert captured['url'].endswith('/v1/inquiries/i1')
    assert 'Bootpay-User-JWT' not in captured['headers']


def test_inquiry_create_is_user_role_even_when_client_role_is_supervisor(commerce, captured):
    """문의 작성은 회원 전용이라 클라이언트 role 과 무관하게 user 로 보낸다."""
    commerce.as_supervisor()
    commerce.inquiry.create(content='언제 배송되나요?', title='배송', product_id='p1', order_id='o1',
                            option='블랙 / M', user_jwt='member-jwt')

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/inquiries')
    assert captured['json'] == {
        'title': '배송',
        'content': '언제 배송되나요?',
        'product_id': 'p1',
        'option': '블랙 / M',
        'order_id': 'o1'
    }
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'


def test_inquiry_update_keeps_empty_title(commerce, captured):
    """title='' 는 제목 삭제 의사다 — compact 가 지우면 안 된다."""
    commerce.inquiry.update('i1', title='', content='수정합니다', login_id='member01')

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/inquiries/i1')
    assert captured['json'] == {'login_id': 'member01', 'title': '', 'content': '수정합니다'}


def test_inquiry_delete_sends_member_query(commerce, captured):
    commerce.inquiry.delete('i1', user_id='u1', supervisor=True)

    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/inquiries/i1?user_id=u1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_inquiry_answer_is_supervisor_only(commerce, captured):
    commerce.inquiry.answer('i1', content='내일 출고됩니다.')

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/inquiries/i1/answer')
    assert captured['json'] == {'content': '내일 출고됩니다.'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_inquiry_ruby_aliases_hit_same_endpoints(commerce, captured):
    commerce.inquiry.inquiries()
    assert '/v1/inquiries?' in captured['url']

    commerce.inquiry.inquiry_detail('i1')
    assert captured['url'].endswith('/v1/inquiries/i1')

    commerce.inquiry.inquiry_create(content='c')
    assert captured['method'] == 'post'

    commerce.inquiry.inquiry_update('i1', content='c')
    assert captured['method'] == 'put'

    commerce.inquiry.inquiry_delete('i1')
    assert captured['method'] == 'delete'

    commerce.inquiry.inquiry_answer('i1', content='a')
    assert captured['url'].endswith('/v1/inquiries/i1/answer')


# ---------------------------------------------------------------------------
# 상품문의 (/v1/product-qnas)
# ---------------------------------------------------------------------------
def test_product_qna_list(commerce, captured):
    commerce.product_qna.list(product_id='p1', user_jwt='member-jwt')

    assert captured['method'] == 'get'
    assert '/v1/product-qnas?' in captured['url']
    assert 'product_id=p1' in captured['url']
    assert 'page=1' in captured['url']
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'


def test_product_qna_list_supervisor_all(commerce, captured):
    commerce.product_qna.list(view='all', supervisor=True)

    assert 'view=all' in captured['url']
    assert 'product_id' not in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_product_qna_detail(commerce, captured):
    commerce.product_qna.detail('q1', login_id='member01', supervisor=True)

    assert captured['url'].endswith('/v1/product-qnas/q1?login_id=member01')
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_product_qna_create_guest(commerce, captured):
    commerce.product_qna.create(product_id='p1', title='재입고 문의', content='재입고 예정이 있나요?',
                                is_secret=True, guest_name='비회원', guest_password='1234')

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/product-qnas')
    assert captured['json'] == {
        'product_id': 'p1',
        'title': '재입고 문의',
        'content': '재입고 예정이 있나요?',
        'is_secret': True,
        'guest_name': '비회원',
        'guest_password': '1234'
    }
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'


def test_product_qna_update_keeps_false_is_secret(commerce, captured):
    """is_secret=False 는 '비밀글 해제' 의사다 — compact 가 지우면 안 된다."""
    commerce.product_qna.update('q1', content='수정합니다', is_secret=False, login_id='member01')

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/product-qnas/q1')
    assert captured['json'] == {'content': '수정합니다', 'is_secret': False, 'login_id': 'member01'}


def test_product_qna_delete_sends_guest_password_in_body(commerce, captured):
    """⚠️ guest_password 는 URL 쿼리가 아니라 본문으로 보낸다."""
    commerce.product_qna.delete('q1', guest_password='1234')

    assert captured['method'] == 'delete'
    assert captured['url'].endswith('/v1/product-qnas/q1')
    assert 'guest_password' not in captured['url']
    assert captured['json'] == {'guest_password': '1234'}


def test_product_qna_answer_is_supervisor_only(commerce, captured):
    commerce.product_qna.answer('q1', content='다음 주 입고 예정입니다.')

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/product-qnas/q1/answer')
    assert captured['json'] == {'content': '다음 주 입고 예정입니다.'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_product_qna_ruby_aliases_hit_same_endpoints(commerce, captured):
    commerce.product_qna.product_qnas(product_id='p1')
    assert '/v1/product-qnas?' in captured['url']

    commerce.product_qna.product_qna_detail('q1')
    assert captured['url'].endswith('/v1/product-qnas/q1')

    commerce.product_qna.product_qna_create(product_id='p1', content='c')
    assert captured['method'] == 'post'

    commerce.product_qna.product_qna_update('q1', content='c')
    assert captured['method'] == 'put'

    commerce.product_qna.product_qna_delete('q1')
    assert captured['method'] == 'delete'

    commerce.product_qna.product_qna_answer('q1', content='a')
    assert captured['url'].endswith('/v1/product-qnas/q1/answer')


# ---------------------------------------------------------------------------
# 상품평 (/v1/reviews)
# ---------------------------------------------------------------------------
def test_review_list(commerce, captured):
    commerce.product_review.list(product_id='p1', user_jwt='member-jwt')

    assert captured['method'] == 'get'
    assert '/v1/reviews?' in captured['url']
    assert 'product_id=p1' in captured['url']
    assert captured['headers']['Bootpay-User-JWT'] == 'member-jwt'
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'


def test_review_list_supervisor(commerce, captured):
    commerce.product_review.list(view='all', user_id='u1', supervisor=True)

    assert 'view=all' in captured['url']
    assert 'user_id=u1' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_review_detail(commerce, captured):
    commerce.product_review.detail('r1')

    assert captured['url'].endswith('/v1/reviews/r1')
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'


def test_review_create(commerce, captured):
    commerce.product_review.create(order_id='o1', product_id='p1', rating=5, content='만족합니다.',
                                   images=['https://cdn.example.com/1.jpg'], login_id='member01')

    assert captured['method'] == 'post'
    assert captured['url'].endswith('/v1/reviews')
    assert captured['json'] == {
        'login_id': 'member01',
        'order_id': 'o1',
        'product_id': 'p1',
        'rating': 5,
        'content': '만족합니다.',
        'images': ['https://cdn.example.com/1.jpg']
    }
    assert captured['headers']['BOOTPAY-ROLE'] == 'user'


def test_review_update_replaces_images(commerce, captured):
    """images 는 보내면 통째로 교체한다 — [] 는 '모두 삭제' 라서 그대로 실어야 한다."""
    commerce.product_review.update('r1', rating=4, images=[])

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/reviews/r1')
    assert captured['json'] == {'rating': 4, 'images': []}


def test_review_delete_sends_reason_as_query(commerce, captured):
    commerce.product_review.delete('r1', reason='광고성 후기', supervisor=True)

    assert captured['method'] == 'delete'
    assert '/v1/reviews/r1?' in captured['url']
    assert 'reason=' in captured['url']
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_review_reply_is_supervisor_only(commerce, captured):
    commerce.product_review.reply('r1', content='소중한 후기 감사합니다.')

    assert captured['method'] == 'put'
    assert captured['url'].endswith('/v1/reviews/r1/reply')
    assert captured['json'] == {'content': '소중한 후기 감사합니다.'}
    assert captured['headers']['BOOTPAY-ROLE'] == 'supervisor'


def test_review_ruby_aliases_hit_same_endpoints(commerce, captured):
    commerce.product_review.reviews()
    assert '/v1/reviews?' in captured['url']

    commerce.product_review.review_detail('r1')
    assert captured['url'].endswith('/v1/reviews/r1')

    commerce.product_review.review_create(order_id='o1', product_id='p1', rating=5, content='c')
    assert captured['method'] == 'post'

    commerce.product_review.review_update('r1', rating=4)
    assert captured['method'] == 'put'

    commerce.product_review.review_delete('r1')
    assert captured['method'] == 'delete'

    commerce.product_review.review_reply('r1', content='감사합니다.')
    assert captured['url'].endswith('/v1/reviews/r1/reply')
