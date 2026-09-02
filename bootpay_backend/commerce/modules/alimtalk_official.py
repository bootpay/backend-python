from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    AlimtalkOfficialListParams,
    AlimtalkOfficialRecommendParams
)


class AlimtalkOfficialModule:
    """
    부트페이 공식 알림톡 템플릿 카탈로그 모듈 (/v1/alimtalk/official 계열)

    부트페이가 미리 카카오 승인을 받아 둔 템플릿이라, 그룹키가 등록된 채널이면 **검수 없이 즉시 발송**된다.
    `alimtalk_sender.create` 로 채널을 등록하면 그룹 등록이 함께 끝나므로 따로 채택할 것이 없다.
    (채택 endpoint 는 서버에서도 비활성화되어 SDK 에 두지 않는다)

    전부 조회 계열이라 부작용이 없다 (자체 DB 만 본다).
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[AlimtalkOfficialListParams] = None):
        """
        공식 템플릿 검색
        GET /v1/alimtalk/official
        keyword 는 본문·이름·분류를 부분일치(대소문자 무시)로 훑는다.
        ⚠️ 서버는 q 를 먼저 보고 없으면 keyword 를 본다 — 정본 키인 q 로 보낸다.
        :param params: 조회 파라미터 (msg_type 은 BA·EX 만 존재한다)
        :return: {'list': [...], 'count': int, 'page': int, 'per': int, 'categories': [...]}
        """
        params = dict(params or {})
        query_params = {
            'q': params.pop('q', None) or params.pop('keyword', None),
            'category': params.get('category'),
            'msg_type': params.get('msg_type'),
            'page': params.get('page'),
            'per': params.get('per'),
            'ksp_id': params.get('ksp_id')
        }

        query = urlencode(self._compact(query_params))
        return self._bootpay.get(
            f'alimtalk/official{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def recommend(self, params: AlimtalkOfficialRecommendParams):
        """
        보내려는 문구로 공식 템플릿을 추천받는다
        POST /v1/alimtalk/official/recommend
        유사도 score(0~1) 내림차순으로 돌려준다.
        :param params: 추천 파라미터 (text 필수)
        :return: 추천 템플릿 목록
        """
        return self._bootpay.post(
            'alimtalk/official/recommend',
            self._compact(params),
            headers=self._alimtalk_headers()
        )

    def detail(self, code: str, ksp_id: Optional[str] = None):
        """
        공식 템플릿 상세 조회
        GET /v1/alimtalk/official/{code}
        :param code: 서버 채번 코드 (슬래시를 포함하지 않는다). 없거나 미노출이면 404(3015).
        :param ksp_id: 주면 그 채널의 변수 예문 사전으로 variable_examples 를 채워 준다 (표시용)
        :return: 공식 템플릿 상세
        """
        query = urlencode(self._compact({'ksp_id': ksp_id}))
        return self._bootpay.get(
            f'alimtalk/official/{code}{"?" + query if query else ""}',
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
