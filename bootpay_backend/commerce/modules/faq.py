import uuid
from typing import TYPE_CHECKING, Optional, List, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource


class FaqModule:
    """
    FAQ 모듈 (/v1/faqs)

    supervisor=True 면 운영자 모드(BOOTPAY-ROLE: supervisor)로 요청한다 — view='all' 로 비공개 FAQ 까지 조회할 수 있다.
    ⚠️ 고객 모드는 몰 FAQ 사용여부가 꺼져 있으면 BOARD_FEATURE_DISABLED 로 거절된다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, page: int = 1, limit: int = 20, keyword: Optional[str] = None, view: Optional[str] = None,
             supervisor: bool = False, idempotency_key: Optional[str] = None):
        """
        FAQ 목록 조회
        GET /v1/faqs
        :param page: 페이지 (기본 1)
        :param limit: 페이지당 건수 (기본 20)
        :param keyword: 제목·본문 검색어
        :param view: 'all' 이면 비공개 FAQ 까지 (supervisor 전용)
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: {'items': List[FAQ], 'total': int}
        """
        query = urlencode(self._compact({
            'page': page,
            'limit': limit,
            'keyword': keyword,
            'view': view
        }))
        return self._bootpay.get(
            f'faqs{"?" + query if query else ""}',
            headers=self._board_headers(supervisor=supervisor, idempotency_key=idempotency_key)
        )

    def detail(self, faq_id: str, supervisor: bool = False, idempotency_key: Optional[str] = None):
        """
        FAQ 단건 조회
        GET /v1/faqs/{faq_id}
        ⚠️ 비공개 FAQ 는 supervisor=True 일 때만 보인다 (아니면 404 POST_NOT_FOUND).
        :param faq_id: FAQ ID
        :param supervisor: 운영자 모드 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: FAQ
        """
        return self._bootpay.get(
            f'faqs/{faq_id}',
            headers=self._board_headers(supervisor=supervisor, idempotency_key=idempotency_key)
        )

    def create(self, title: str, content: str, images: Optional[List[Any]] = None,
               is_display: Optional[bool] = None, idempotency_key: Optional[str] = None):
        """
        FAQ 등록 (supervisor 전용)
        POST /v1/faqs
        :param title: 제목
        :param content: 본문
        :param images: 이미지 목록
        :param is_display: 노출 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: FAQ
        """
        return self._bootpay.post(
            'faqs',
            self._compact({
                'title': title,
                'content': content,
                'images': images,
                'is_display': is_display
            }),
            headers=self._board_headers(supervisor=True, idempotency_key=idempotency_key)
        )

    def update(self, faq_id: str, title: Optional[str] = None, content: Optional[str] = None,
               images: Optional[List[Any]] = None, is_display: Optional[bool] = None,
               idempotency_key: Optional[str] = None):
        """
        FAQ 수정 (supervisor 전용)
        PUT /v1/faqs/{faq_id}
        보낸 필드만 바뀐다. ⚠️ images 는 보내면 목록 전체를 교체한다 ([] 면 모두 삭제).
        :param faq_id: FAQ ID
        :param title: 제목
        :param content: 본문
        :param images: 이미지 목록 (전체 교체)
        :param is_display: 노출 여부
        :param idempotency_key: 미지정시 자동 생성
        :return: FAQ
        """
        return self._bootpay.put(
            f'faqs/{faq_id}',
            self._compact({
                'title': title,
                'content': content,
                'images': images,
                'is_display': is_display
            }),
            headers=self._board_headers(supervisor=True, idempotency_key=idempotency_key)
        )

    def delete(self, faq_id: str, idempotency_key: Optional[str] = None):
        """
        FAQ 삭제 (supervisor 전용)
        DELETE /v1/faqs/{faq_id}
        :param faq_id: FAQ ID
        :param idempotency_key: 미지정시 자동 생성
        :return: 삭제 결과
        """
        return self._bootpay.delete(
            f'faqs/{faq_id}',
            headers=self._board_headers(supervisor=True, idempotency_key=idempotency_key)
        )

    def _compact(self, payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """None 값을 제거한다 (False 는 남긴다)."""
        return {k: v for k, v in (payload or {}).items() if v is not None}

    def _board_headers(self, supervisor: bool = False, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        게시판 요청 헤더
        Idempotency-Key 는 미지정시 매 호출마다 생성되고, BOOTPAY-ROLE 은 supervisor 여부로 정해진다
        (공통 계층의 role 이 요청별 role 을 덮어쓰지 않도록 항상 명시한다).
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor' if supervisor else 'user'
        }

    # ruby SDK 와 같은 이름으로도 호출할 수 있게 별칭을 둔다 (동기화 파이프라인 호환)
    faqs = list
    faq_detail = detail
    faq_create = create
    faq_update = update
    faq_delete = delete
