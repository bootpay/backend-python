from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    AlimtalkMessageListParams,
    AlimtalkMessageStatsParams
)


class AlimtalkMessageModule:
    """
    알림톡 발송내역·집계 모듈 (GET /v1/alimtalk/messages 계열)

    **유료** 알림톡만 조회된다 (무료 커머스 알림톡은 포함되지 않는다).
    상태는 벤더 결과 동기화로 확정되므로 접수 직후에는 requested 로 보인다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[AlimtalkMessageListParams] = None):
        """
        발송내역 목록 조회
        GET /v1/alimtalk/messages
        ⚠️ 기간 기본값은 최근 30일이고 최대 조회 폭은 92일이다 — 초과분은 거부하지 않고 시작일을 당겨 잘라낸다.
           실제 적용된 구간은 응답의 period 로 확인한다.
        :param params: 조회 파라미터 (status: requested·success·failed·canceled)
        :return: {'list': [...], 'count': int, 'page': int, 'per': int, 'period': {'from':, 'to':}}
        """
        query = urlencode(self._query(params))
        return self._bootpay.get(
            f'alimtalk/messages{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def stats(self, params: Optional[AlimtalkMessageStatsParams] = None):
        """
        기간 집계 조회
        GET /v1/alimtalk/messages/stats
        일자별 집계 원장에서 읽으므로 응답이 빠르다.
        ⚠️ billing.unit_price_source 가 'default' 면 **잠정 단가**다 (확정 청구액이 아니다).
        ⚠️ billable_count 는 성공 − 폴백이다 — 폴백분은 LMS 단가로 따로 계산된다.
        :param params: 조회 기간
        :return: {'period':, 'totals': {...}, 'daily': [...], 'billing': {...}}
        """
        query = urlencode(self._query(params))
        return self._bootpay.get(
            f'alimtalk/messages/stats{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def detail(self, receipt_id: str):
        """
        단건 발송 결과 조회
        GET /v1/alimtalk/messages/{receipt_id}
        실패 사유는 error_code·error_message 에 담긴다.
        fallback_type 은 폴백이 꺼진 건이면 None, 켜진 건이면 LMS 다.
        다른 프로젝트의 건이거나 없으면 404(3025).
        :param receipt_id: 발송 접수 ID
        :return: 발송 상세
        """
        return self._bootpay.get(
            f'alimtalk/messages/{receipt_id}',
            headers=self._alimtalk_headers()
        )

    def _query(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        None 을 제거하고 bool 을 소문자 'true'/'false' 로 직렬화한다.
        ⚠️ urlencode 는 True 를 'True' 로 쓴다 — Rails 의 boolean 캐스팅은 'False' 를 참으로 읽으므로
           그대로 보내면 false 가 true 로 뒤집힌다.
        """
        query = {}
        for key, value in (params or {}).items():
            if value is None:
                continue
            query[key] = ('true' if value else 'false') if isinstance(value, bool) else value
        return query

    def _alimtalk_headers(self) -> Dict[str, str]:
        """
        알림톡 API 요청 헤더
        ★Idempotency-Key 를 싣지 않는다★ 알림톡 API 는 이 헤더를 읽지 않는다
          (멱등은 발송의 ref_id 로만 성립한다).
        ★BOOTPAY-ROLE 은 항상 user★ 알림톡 스코프 키가 전부 user:alimtalk_* 다.
        """
        return {'BOOTPAY-ROLE': 'user'}
