from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    AlimtalkOptoutListParams,
    AlimtalkOptoutCreateParams,
    AlimtalkOptoutCheckParams
)


class AlimtalkOptoutModule:
    """
    알림톡 수신거부 모듈 (/v1/alimtalk/optouts 계열, 가맹점 CRM 수신거부 동기화용)

    발송 판정과 **같은 기준**으로 다룬다 — 부트페이 전역(global) + 내 프로젝트.
    ⚠️ 전역 건은 **조회는 되지만 해제할 수 없다** (releasable: False).
       이걸 노출하지 않으면 "화면엔 수신거부가 아닌데 발송은 3021 로 막히는" 상태가 된다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[AlimtalkOptoutListParams] = None):
        """
        수신거부 목록 조회
        GET /v1/alimtalk/optouts
        phone 은 숫자만 남겨 **부분일치**로 찾는다 (정확 매칭이 아니다). 50건 단위로 페이징된다.
        :param params: 조회 파라미터
        :return: {'list': [{'id':, 'phone':, 'scope':, 'global':, 'releasable':, 'source':,
                            'reason':, 'opted_out_at':, 'created_at':}], 'count': int, 'page': int}
        """
        query = urlencode(self._compact(params))
        return self._bootpay.get(
            f'alimtalk/optouts{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def create(self, params: AlimtalkOptoutCreateParams):
        """
        수신거부 등록
        POST /v1/alimtalk/optouts
        내 프로젝트 스코프로 등록된다 (source: api). 같은 번호를 다시 등록해도 멱등이다.
        :param params: 등록 파라미터 (phone 필수)
        :return: 등록된 수신거부
        """
        return self._bootpay.post(
            'alimtalk/optouts',
            self._compact(params),
            headers=self._alimtalk_headers()
        )

    def check(self, params: AlimtalkOptoutCheckParams):
        """
        발송 전 수신거부 사전 확인
        POST /v1/alimtalk/optouts/check
        발송 판정과 **같은 축**으로 대조하므로, 벌크에서 skipped 로 낭비될 건을 미리 뺄 수 있다.
        단건(phone)·다건(phones) 모두 받는다.
        ⚠️ 1회 최대 1,000건이고 넘으면 -48 이다 (중복은 서버가 제거).
        :param params: 확인 파라미터
        :return: {'list': [{'phone':, 'opted_out':, 'global':, 'releasable':, 'opted_out_at':}],
                  'count': int, 'opted_out_count': int}
        """
        return self._bootpay.post(
            'alimtalk/optouts/check',
            self._compact(params),
            headers=self._alimtalk_headers()
        )

    def release(self, phone: str):
        """
        수신거부 해제
        DELETE /v1/alimtalk/optouts/{phone}
        내 프로젝트 스코프 건만 해제되며 멱등이다 (없어도 성공).
        ⚠️ 전역 차단은 해제되지 않고 global_blocked: True 로 알려 준다 —
           "지웠는데 여전히 막히는" 상태를 응답으로 드러내기 위함이다.
        :param phone: 해제할 수신번호
        :return: {'phone':, 'released':, 'global_blocked':}
        """
        return self._bootpay.delete(
            f'alimtalk/optouts/{phone}',
            headers=self._alimtalk_headers()
        )

    def _compact(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """None 값을 제거한다."""
        return {k: v for k, v in (params or {}).items() if v is not None}

    def _alimtalk_headers(self) -> Dict[str, str]:
        """
        알림톡 API 요청 헤더
        ★Idempotency-Key 를 싣지 않는다★ 알림톡 API 는 이 헤더를 읽지 않는다.
        ★BOOTPAY-ROLE 은 항상 user★ 알림톡 스코프 키가 전부 user:alimtalk_* 다.
        """
        return {'BOOTPAY-ROLE': 'user'}
