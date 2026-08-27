from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    AlimtalkSenderOtpParams,
    AlimtalkSenderCreateParams
)


class AlimtalkSenderModule:
    """
    알림톡 발신프로필(카카오채널) 생명주기 모듈 (GET /v1/alimtalk/categories · /senders 계열)

    카테고리 조회 → OTP 발송 → 발신프로필 등록 → 목록/상세 → 연동 해지 순으로 쓴다.
    등록이 끝나면 서버가 그룹키 등록까지 자동으로 하므로, 공식 템플릿은 별도 채택 없이 바로 발송된다.

    ⚠️ 실제 부작용: `otp` 는 채널 관리자 휴대폰으로 **문자를 실제 발송**하고,
       `create` 는 카카오에 발신프로필을 **실제 등록**한다. 샌드박스가 없다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def categories(self):
        """
        카카오 카테고리 목록 조회
        GET /v1/alimtalk/categories
        발신프로필 등록 시 필요한 category_code 후보다. 벤더 응답을 그대로 프록시한다.
        :return: 카테고리 목록
        """
        return self._bootpay.get('alimtalk/categories', headers=self._alimtalk_headers())

    def otp(self, params: AlimtalkSenderOtpParams):
        """
        채널 관리자폰으로 OTP 발송
        POST /v1/alimtalk/senders/otp
        ⚠️ 실제로 문자가 나간다. 여기서 받은 인증번호를 `create` 의 otp 로 넘긴다.
        :param params: {'yellow_id': '@채널아이디', 'phone': '01012345678'}
        :return: 발송 결과
        """
        return self._bootpay.post(
            'alimtalk/senders/otp',
            self._compact(params),
            headers=self._alimtalk_headers()
        )

    def create(self, params: AlimtalkSenderCreateParams):
        """
        발신프로필 등록
        POST /v1/alimtalk/senders
        ⚠️ 카카오에 발신프로필이 실제 등록된다. 같은 yellow_id 를 다시 등록하면 기존 프로필을 재사용한다(dedup).
        등록 성공 시 그룹키 등록까지 서버가 수행하므로 공식 카탈로그 전체를 바로 발송할 수 있다.
        :param params: {'otp':, 'yellow_id':, 'phone':, 'category_code':}
        :return: 등록된 발신프로필
        """
        return self._bootpay.post(
            'alimtalk/senders',
            self._compact(params),
            headers=self._alimtalk_headers()
        )

    def list(self):
        """
        연동한 채널 목록 조회
        GET /v1/alimtalk/senders
        자체 DB 만 조회하며 벤더를 호출하지 않는다.
        :return: {'list': [...], 'count': int}
        """
        return self._bootpay.get('alimtalk/senders', headers=self._alimtalk_headers())

    def detail(self, ksp_id: str, sync: Optional[bool] = None):
        """
        채널 상세 조회
        GET /v1/alimtalk/senders/{ksp_id}
        ⚠️ 미연동/미존재 채널은 404, 다른 프로젝트의 채널은 403 으로 오며 둘 다 error_code 는 3024 다.
        :param ksp_id: 채널 문서 ID
        :param sync: True 면 벤더에서 채널 상태를 다시 읽어 반영한다(느리다). 미지정이면 자체 DB 만 본다.
        :return: 채널 상세
        """
        query = urlencode(self._query({'sync': sync}))
        return self._bootpay.get(
            f'alimtalk/senders/{ksp_id}{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def release(self, ksp_id: str):
        """
        채널 연동 해지
        DELETE /v1/alimtalk/senders/{ksp_id}
        이 프로젝트와의 연동만 끊는다 — 채널 모델과 템플릿은 보존된다. 성공 시 본문은 null 이다.
        :param ksp_id: 채널 문서 ID
        :return: None
        """
        return self._bootpay.delete(
            f'alimtalk/senders/{ksp_id}',
            headers=self._alimtalk_headers()
        )

    def variable_examples(self, ksp_id: str, examples: Dict[str, str]):
        """
        채널 변수 예문 사전 갱신
        PUT /v1/alimtalk/senders/{ksp_id}/variable_examples
        템플릿 미리보기에서 #{user_name} 대신 '홍길동' 처럼 읽히게 하는 **표시용** 값이다.
        ⚠️ 발송값이 아니다 — 벤더로 전송되지 않으므로 검수 상태와 무관하다. 보낸 키만 덮어쓴다(부분 갱신).
        :param ksp_id: 채널 문서 ID
        :param examples: {'user_name': '홍길동', 'company_name': '부트페이몰'}
                         — 키에 '.' 이나 선행 '$' 는 쓸 수 없다.
        :return: 갱신된 예문 사전
        """
        return self._bootpay.put(
            f'alimtalk/senders/{ksp_id}/variable_examples',
            self._compact({'examples': examples}),
            headers=self._alimtalk_headers()
        )

    def _compact(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """None 값을 제거한다."""
        return {k: v for k, v in (params or {}).items() if v is not None}

    def _query(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        None 을 제거하고 bool 을 소문자 'true'/'false' 로 직렬화한다.
        ⚠️ urlencode 는 True 를 'True' 로 쓴다 — Rails 의 boolean 캐스팅은 'False' 를 참으로 읽으므로
           그대로 보내면 sync=false 가 sync=true 로 뒤집힌다.
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
          (멱등은 발송의 ref_id 로만 성립한다). invoice/product 처럼 무조건 붙이면
          서버가 주지 않는 보장을 주는 것처럼 보인다.
        ★BOOTPAY-ROLE 은 항상 user★ 알림톡 스코프 키가 전부 user:alimtalk_* 다.
        """
        return {'BOOTPAY-ROLE': 'user'}
