import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource


class InquiryModule:
    """
    1:1 문의 모듈 (/v1/inquiries)

    회원 모드: user_id(Bootpay 회원 _id 또는 외부 회원 ID)·login_id·user_jwt 중 하나로 회원을 정하고 본인 문의만 본다.
    supervisor=True 면 몰 전체 문의를 다룬다 — 이때 user_id 는 작성 회원 필터(선택)다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, user_id: Optional[str] = None, login_id: Optional[str] = None, user_jwt: Optional[str] = None,
             answered: Optional[bool] = None, page: int = 1, limit: int = 20, supervisor: bool = False,
             idempotency_key: Optional[str] = None):
        """
        1:1 문의 목록 조회
        GET /v1/inquiries
        :param user_id: 회원 ID (Bootpay 회원 _id 또는 외부 회원 ID)
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param answered: True 답변 완료만 / False 미답변만 / None 전체
        :param page: 페이지 (기본 1)
        :param limit: 페이지당 건수 (기본 20)
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: {'items': List[Inquiry], 'total': int}
        """
        query = urlencode(self._compact({
            'user_id': user_id,
            'login_id': login_id,
            # ⚠️ bool 은 소문자 'true'/'false' 로 보낸다 — 'True' 는 Rails 캐스팅 대상이 아니다.
            'answered': None if answered is None else ('true' if answered else 'false'),
            'page': page,
            'limit': limit
        }))
        return self._bootpay.get(
            f'inquiries{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def detail(self, inquiry_id: str, user_id: Optional[str] = None, login_id: Optional[str] = None,
               user_jwt: Optional[str] = None, supervisor: bool = False, idempotency_key: Optional[str] = None):
        """
        1:1 문의 단건 조회
        GET /v1/inquiries/{inquiry_id}
        회원 모드는 작성 회원 본인 문의만 보인다 (다른 회원 문의는 404). supervisor=True 면 몰의 모든 문의.
        :param inquiry_id: 문의 ID
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: Inquiry
        """
        query = urlencode(self._compact({'user_id': user_id, 'login_id': login_id}))
        return self._bootpay.get(
            f'inquiries/{inquiry_id}{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def create(self, content: str, user_id: Optional[str] = None, login_id: Optional[str] = None,
               user_jwt: Optional[str] = None, title: Optional[str] = None, product_id: Optional[str] = None,
               option: Optional[str] = None, order_id: Optional[str] = None,
               idempotency_key: Optional[str] = None):
        """
        1:1 문의 작성 (회원 전용)
        POST /v1/inquiries
        ⚠️ product_id 는 이 몰의 상품, order_id 는 작성 회원의 주문이어야 한다.
           option 은 상품 옵션 문구다 (product_id 가 함께 필요하다).
        :param content: 문의 본문
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param title: 제목
        :param product_id: 문의 대상 상품 ID
        :param option: 상품 옵션 문구
        :param order_id: 문의 대상 주문 ID
        :param idempotency_key: 미지정시 자동 생성
        :return: Inquiry
        """
        return self._bootpay.post(
            'inquiries',
            self._compact({
                'user_id': user_id,
                'login_id': login_id,
                'title': title,
                'content': content,
                'product_id': product_id,
                'option': option,
                'order_id': order_id
            }),
            headers=self._board_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def update(self, inquiry_id: str, user_id: Optional[str] = None, login_id: Optional[str] = None,
               user_jwt: Optional[str] = None, title: Optional[str] = None, content: Optional[str] = None,
               idempotency_key: Optional[str] = None):
        """
        1:1 문의 수정 (작성 회원 본인, 답변 전만)
        PUT /v1/inquiries/{inquiry_id}
        ⚠️ 답변이 달린 문의는 409 INQUIRY_ALREADY_ANSWERED. title 에 '' 를 보내면 제목을 지운다.
        :param inquiry_id: 문의 ID
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param title: 제목 ('' 이면 제목 삭제)
        :param content: 문의 본문
        :param idempotency_key: 미지정시 자동 생성
        :return: Inquiry
        """
        return self._bootpay.put(
            f'inquiries/{inquiry_id}',
            self._compact({
                'user_id': user_id,
                'login_id': login_id,
                'title': title,
                'content': content
            }),
            headers=self._board_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def delete(self, inquiry_id: str, user_id: Optional[str] = None, login_id: Optional[str] = None,
               user_jwt: Optional[str] = None, supervisor: bool = False, idempotency_key: Optional[str] = None):
        """
        1:1 문의 삭제 (작성 회원 본인 또는 supervisor)
        DELETE /v1/inquiries/{inquiry_id}
        달린 답변도 함께 삭제된다.
        :param inquiry_id: 문의 ID
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: 삭제 결과
        """
        query = urlencode(self._compact({'user_id': user_id, 'login_id': login_id}))
        return self._bootpay.delete(
            f'inquiries/{inquiry_id}{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def answer(self, inquiry_id: str, content: str, idempotency_key: Optional[str] = None):
        """
        1:1 문의 답변 등록·수정 (supervisor 전용)
        PUT /v1/inquiries/{inquiry_id}/answer
        답변이 없으면 만들고, 있으면 내용을 바꾼다. 응답은 답변이 반영된 문의 객체다.
        :param inquiry_id: 문의 ID
        :param content: 답변 본문
        :param idempotency_key: 미지정시 자동 생성
        :return: Inquiry
        """
        return self._bootpay.put(
            f'inquiries/{inquiry_id}/answer',
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
    inquiries = list
    inquiry_detail = detail
    inquiry_create = create
    inquiry_update = update
    inquiry_delete = delete
    inquiry_answer = answer
