import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource


class ProductQnaModule:
    """
    상품문의 모듈 (/v1/product-qnas)

    고객 모드는 product_id 가 필수다. 다른 사람의 비밀글은 is_viewable: False 로 본문 없이 온다.
    회원(user_id·login_id·user_jwt)을 보내면 그 회원이 쓴 비밀글 본문이 보인다.
    supervisor=True + view='all' 이면 몰 전체(숨김 포함) — 이때 product_id 는 선택 필터다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, product_id: Optional[str] = None, view: Optional[str] = None, page: int = 1, limit: int = 20,
             user_id: Optional[str] = None, login_id: Optional[str] = None, user_jwt: Optional[str] = None,
             supervisor: bool = False, idempotency_key: Optional[str] = None):
        """
        상품문의 목록 조회
        GET /v1/product-qnas
        ⚠️ 고객 모드는 product_id 가 필수다 (supervisor + view='all' 일 때만 선택 필터가 된다).
        :param product_id: 상품 ID
        :param view: 'all' 이면 몰 전체(숨김 포함, supervisor 전용)
        :param page: 페이지 (기본 1)
        :param limit: 페이지당 건수 (기본 20)
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: {'items': List[ProductQna], 'total': int}
        """
        query = urlencode(self._compact({
            'product_id': product_id,
            'view': view,
            'page': page,
            'limit': limit,
            'user_id': user_id,
            'login_id': login_id
        }))
        return self._bootpay.get(
            f'product-qnas{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def detail(self, product_qna_id: str, user_id: Optional[str] = None, login_id: Optional[str] = None,
               user_jwt: Optional[str] = None, supervisor: bool = False, idempotency_key: Optional[str] = None):
        """
        상품문의 단건 조회
        GET /v1/product-qnas/{product_qna_id}
        ⚠️ 다른 사람의 비밀글은 403 PRODUCT_QNA_SECRET_FORBIDDEN.
           supervisor=True 면 비밀글·숨김 글도 본다.
        :param product_qna_id: 상품문의 ID
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: ProductQna
        """
        query = urlencode(self._compact({'user_id': user_id, 'login_id': login_id}))
        return self._bootpay.get(
            f'product-qnas/{product_qna_id}{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def create(self, product_id: str, content: str, title: Optional[str] = None,
               product_option_id: Optional[str] = None, option_text: Optional[str] = None,
               is_secret: Optional[bool] = None, guest_name: Optional[str] = None,
               guest_password: Optional[str] = None, user_id: Optional[str] = None,
               login_id: Optional[str] = None, user_jwt: Optional[str] = None,
               idempotency_key: Optional[str] = None):
        """
        상품문의 작성
        POST /v1/product-qnas
        회원(user_id·login_id·user_jwt) 또는 비회원(guest_name + guest_password, 몰이 비회원 작성을 허용할 때).
        ⚠️ 회원 문의면 guest_* 는 무시된다.
        :param product_id: 상품 ID
        :param content: 문의 본문
        :param title: 제목
        :param product_option_id: 상품 옵션 ID
        :param option_text: 상품 옵션 문구
        :param is_secret: 비밀글 여부
        :param guest_name: 비회원 작성자명
        :param guest_password: 비회원 비밀번호
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param idempotency_key: 미지정시 자동 생성
        :return: ProductQna
        """
        return self._bootpay.post(
            'product-qnas',
            self._compact({
                'product_id': product_id,
                'title': title,
                'content': content,
                'product_option_id': product_option_id,
                'option_text': option_text,
                'is_secret': is_secret,
                'guest_name': guest_name,
                'guest_password': guest_password,
                'user_id': user_id,
                'login_id': login_id
            }),
            headers=self._board_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def update(self, product_qna_id: str, title: Optional[str] = None, content: Optional[str] = None,
               is_secret: Optional[bool] = None, guest_password: Optional[str] = None,
               user_id: Optional[str] = None, login_id: Optional[str] = None, user_jwt: Optional[str] = None,
               idempotency_key: Optional[str] = None):
        """
        상품문의 수정 (작성 회원 본인 또는 비회원 비밀번호, 답변 전만)
        PUT /v1/product-qnas/{product_qna_id}
        ⚠️ 답변이 달린 문의는 409 PRODUCT_QNA_ALREADY_ANSWERED,
           비회원 비밀번호가 틀리면 403 PRODUCT_QNA_GUEST_PASSWORD_INVALID.
        :param product_qna_id: 상품문의 ID
        :param title: 제목
        :param content: 문의 본문
        :param is_secret: 비밀글 여부
        :param guest_password: 비회원 비밀번호
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param idempotency_key: 미지정시 자동 생성
        :return: ProductQna
        """
        return self._bootpay.put(
            f'product-qnas/{product_qna_id}',
            self._compact({
                'title': title,
                'content': content,
                'is_secret': is_secret,
                'guest_password': guest_password,
                'user_id': user_id,
                'login_id': login_id
            }),
            headers=self._board_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def delete(self, product_qna_id: str, guest_password: Optional[str] = None, user_id: Optional[str] = None,
               login_id: Optional[str] = None, user_jwt: Optional[str] = None, supervisor: bool = False,
               idempotency_key: Optional[str] = None):
        """
        상품문의 삭제 (작성 회원 본인·비회원 비밀번호 또는 supervisor)
        DELETE /v1/product-qnas/{product_qna_id}
        ⚠️ guest_password 는 URL 쿼리가 아닌 본문으로 보낸다 (서버는 둘 다 받는다).
        :param product_qna_id: 상품문의 ID
        :param guest_password: 비회원 비밀번호
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: 삭제 결과
        """
        return self._bootpay.delete(
            f'product-qnas/{product_qna_id}',
            data=self._compact({
                'guest_password': guest_password,
                'user_id': user_id,
                'login_id': login_id
            }),
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def answer(self, product_qna_id: str, content: str, idempotency_key: Optional[str] = None):
        """
        상품문의 답변 등록·수정 (supervisor 전용)
        PUT /v1/product-qnas/{product_qna_id}/answer
        답변이 없으면 만들고, 있으면 내용을 바꾼다. 응답은 답변이 반영된 상품문의 객체다.
        :param product_qna_id: 상품문의 ID
        :param content: 답변 본문
        :param idempotency_key: 미지정시 자동 생성
        :return: ProductQna
        """
        return self._bootpay.put(
            f'product-qnas/{product_qna_id}/answer',
            {'content': content},
            headers=self._board_headers(supervisor=True, idempotency_key=idempotency_key)
        )

    def _compact(self, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """None 값을 제거한다 (False 는 남긴다)."""
        return {k: v for k, v in (payload or {}).items() if v is not None}

    def _board_headers(self, supervisor: bool = False, user_jwt: Optional[str] = None,
                       idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        게시판 요청 헤더
        Idempotency-Key 는 미지정시 매 호출마다 생성되고, BOOTPAY-ROLE 은 supervisor 여부로 정해진다
        (공통 계층의 role 이 요청별 role 을 덮어쓰지 않도록 항상 명시한다).
        Bootpay-User-JWT 는 값이 있을 때만 붙는다.
        """
        headers = {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor' if supervisor else 'user'
        }
        if user_jwt:
            headers['Bootpay-User-JWT'] = user_jwt
        return headers

    # ruby SDK 와 같은 이름으로도 호출할 수 있게 별칭을 둔다 (동기화 파이프라인 호환)
    product_qnas = list
    product_qna_detail = detail
    product_qna_create = create
    product_qna_update = update
    product_qna_delete = delete
    product_qna_answer = answer
