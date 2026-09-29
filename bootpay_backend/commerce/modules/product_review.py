import uuid
from typing import TYPE_CHECKING, Optional, List, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource


class ProductReviewModule:
    """
    상품평 모듈 (/v1/reviews)

    회원 모드: user_id·login_id·user_jwt 로 정한 회원이 쓴 상품평만 본다.
    supervisor=True 면 몰 전체 상품평 — 이때 user_id 는 작성 회원 필터(선택)다.
    ⚠️ 상품 상세의 공개 상품평 목록은 기존 GET /v1/products/{product_id}/reviews 를 쓴다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, page: int = 1, limit: int = 20, product_id: Optional[str] = None, view: Optional[str] = None,
             user_id: Optional[str] = None, login_id: Optional[str] = None, user_jwt: Optional[str] = None,
             supervisor: bool = False, idempotency_key: Optional[str] = None):
        """
        상품평 목록 조회
        GET /v1/reviews
        :param page: 페이지 (기본 1)
        :param limit: 페이지당 건수 (기본 20)
        :param product_id: 상품 ID 필터
        :param view: 'all' 이면 숨김 상품평까지 (supervisor 전용)
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: {'items': List[ProductReview], 'total': int}
        """
        query = urlencode(self._compact({
            'page': page,
            'limit': limit,
            'product_id': product_id,
            'view': view,
            'user_id': user_id,
            'login_id': login_id
        }))
        return self._bootpay.get(
            f'reviews{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def detail(self, product_review_id: str, user_id: Optional[str] = None, login_id: Optional[str] = None,
               user_jwt: Optional[str] = None, supervisor: bool = False, idempotency_key: Optional[str] = None):
        """
        상품평 단건 조회
        GET /v1/reviews/{product_review_id}
        공개 상품평은 누구나, 숨김 상품평은 작성 회원 본인 또는 supervisor 만 본다.
        :param product_review_id: 상품평 ID
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: ProductReview
        """
        query = urlencode(self._compact({'user_id': user_id, 'login_id': login_id}))
        return self._bootpay.get(
            f'reviews/{product_review_id}{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def create(self, order_id: str, product_id: str, rating: int, content: str,
               product_option_id: Optional[str] = None, images: Optional[List[Any]] = None,
               user_id: Optional[str] = None, login_id: Optional[str] = None, user_jwt: Optional[str] = None,
               idempotency_key: Optional[str] = None):
        """
        상품평 작성 (회원 전용)
        POST /v1/reviews
        ⚠️ order_id 는 회원의 구매확정 주문, product_id(·product_option_id)는 그 주문에 담긴 상품이어야 한다.
           images 는 사진 URL 최대 5개(문자열 또는 {'url': ...} 딕셔너리)다 — 파일 업로드는 지원하지 않는다.
        :param order_id: 주문 ID
        :param product_id: 상품 ID
        :param rating: 별점
        :param content: 상품평 본문
        :param product_option_id: 상품 옵션 ID
        :param images: 사진 URL 목록 (최대 5개)
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param idempotency_key: 미지정시 자동 생성
        :return: ProductReview
        """
        return self._bootpay.post(
            'reviews',
            self._compact({
                'user_id': user_id,
                'login_id': login_id,
                'order_id': order_id,
                'product_id': product_id,
                'product_option_id': product_option_id,
                'rating': rating,
                'content': content,
                'images': images
            }),
            headers=self._board_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def update(self, product_review_id: str, rating: Optional[int] = None, content: Optional[str] = None,
               images: Optional[List[Any]] = None, user_id: Optional[str] = None, login_id: Optional[str] = None,
               user_jwt: Optional[str] = None, idempotency_key: Optional[str] = None):
        """
        상품평 수정 (작성 회원 본인, 작성 후 7일 이내)
        PUT /v1/reviews/{product_review_id}
        ⚠️ images 는 보내면 통째로 교체한다 ([] 면 모두 삭제). 7일이 지나면 REVIEW_EDIT_TIME_EXPIRED.
        :param product_review_id: 상품평 ID
        :param rating: 별점
        :param content: 상품평 본문
        :param images: 사진 URL 목록 (전체 교체)
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param idempotency_key: 미지정시 자동 생성
        :return: ProductReview
        """
        return self._bootpay.put(
            f'reviews/{product_review_id}',
            self._compact({
                'user_id': user_id,
                'login_id': login_id,
                'rating': rating,
                'content': content,
                'images': images
            }),
            headers=self._board_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def delete(self, product_review_id: str, reason: Optional[str] = None, user_id: Optional[str] = None,
               login_id: Optional[str] = None, user_jwt: Optional[str] = None, supervisor: bool = False,
               idempotency_key: Optional[str] = None):
        """
        상품평 삭제 (작성 회원 본인 또는 supervisor)
        DELETE /v1/reviews/{product_review_id}
        ⚠️ 지급된 적립금 회수·상품 통계 차감이 함께 일어난다. reason 은 운영자 모드의 삭제 사유다.
        :param product_review_id: 상품평 ID
        :param reason: 삭제 사유 (supervisor 전용)
        :param user_id: 회원 ID
        :param login_id: 회원 로그인 ID
        :param user_jwt: 회원 JWT
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: 삭제 결과
        """
        query = urlencode(self._compact({
            'user_id': user_id,
            'login_id': login_id,
            'reason': reason
        }))
        return self._bootpay.delete(
            f'reviews/{product_review_id}{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def reply(self, product_review_id: str, content: str, idempotency_key: Optional[str] = None):
        """
        상품평 판매자 답글 등록·수정 (supervisor 전용)
        PUT /v1/reviews/{product_review_id}/reply
        답글이 없으면 만들고, 있으면 내용을 바꾼다 (10자 이상). 응답은 답글이 반영된 상품평 객체다.
        :param product_review_id: 상품평 ID
        :param content: 답글 본문 (10자 이상)
        :param idempotency_key: 미지정시 자동 생성
        :return: ProductReview
        """
        return self._bootpay.put(
            f'reviews/{product_review_id}/reply',
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
    reviews = list
    review_detail = detail
    review_create = create
    review_update = update
    review_delete = delete
    review_reply = reply
