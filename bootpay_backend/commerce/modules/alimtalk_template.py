from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    AlimtalkTemplateListParams,
    AlimtalkTemplateCreateParams,
    AlimtalkTemplateUpdateParams,
    AlimtalkTemplateExportParams
)


class AlimtalkTemplateModule:
    """
    가맹점 자체 알림톡 템플릿 CRUD·등록·검수 모듈 (/v1/alimtalk/templates 계열)

    흐름: (초안 생성 → 확인 → 대행사 등록) → 검수 요청 → 승인(APR) → 발송 가능
      `create({'register': False, ...})` 로 초안만 만들고, 내용을 확인한 뒤
      `register` 로 올리는 것을 권장한다.

    ⚠️ `register` 를 명시적으로 False 로 주지 않으면 **생성 즉시 대행사·카카오에 실제 등록**된다.
    ⚠️ 본문 변수는 `#{변수명}` 형식이고 템플릿 전체에서 최대 40개다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[AlimtalkTemplateListParams] = None):
        """
        내 자체 템플릿 목록 조회
        GET /v1/alimtalk/templates
        ins: 검수상태 필터 — 1 REG(등록) / 2 REQ(검수요청) / 3 APR(승인) / 4 KRR(등록거절) / 5 REJ(승인반려).
             숫자·숫자문자열·벤더 문자열('APR' 등)을 모두 받는다. 해석 못 하는 값은 필터 없음으로 떨어진다.
        ⚠️ 페이지네이션이 없다 — 필터에 걸린 템플릿을 한 번에 모두 돌려준다.
        :param params: 조회 파라미터 (sort: latest(기본)·oldest·code)
        :return: 템플릿 목록
        """
        query = urlencode(self._query(params))
        return self._bootpay.get(
            f'alimtalk/templates{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def create(self, params: AlimtalkTemplateCreateParams):
        """
        자체 템플릿 생성
        POST /v1/alimtalk/templates
        ⚠️ register 를 False 로 주지 않으면 대행사·카카오에 **실제 등록**된다 (되돌리려면 삭제해야 한다).

        emphasize_type: NONE·TEXT(강조표기형)·IMAGE(이미지형)·ITEM_LIST(아이템리스트형)
          - TEXT 는 emphasize_title·emphasize_subtitle 둘 다 필수 (각 50자·40자)
          - IMAGE 는 이미지 필수 — `image` 로 올린 URL 을 storage_image_url 로 넘긴다
          - ITEM_LIST 는 template_item.list(2~10개) 필수 + template_header·item_highlight·이미지 중 하나 이상
        msg_type: BA(기본형)·EX(부가정보형, template_extra 필수)·AD(채널추가형)·MI(복합형)
          - AD·MI 는 채널추가(AC) 버튼이 필수다
        examples: 변수 예문(표시용). 주면 **모든 변수에 예문이 있어야** 한다 (없으면 3017).
        :param params: 템플릿 정보 (ksp_id 필수. 여기 명시되지 않은 값도 서버로 그대로 전달된다)
        :return: 생성된 템플릿
        """
        return self._bootpay.post(
            'alimtalk/templates',
            self._compact(params),
            headers=self._alimtalk_headers()
        )

    def detail(self, template_id: str, sync: Optional[bool] = None):
        """
        자체 템플릿 상세 조회
        GET /v1/alimtalk/templates/{template_id}
        :param template_id: 문서 ID. ObjectId 형식이 아니면 **템플릿 코드**로 해석한다.
        :param sync: ⚠️ 서버 기본값이 **True** 라 조회만 해도 벤더 상태 동기화가 일어난다.
                     초안(등록 전)을 조회할 때는 False 를 권장한다.
        :return: 템플릿 상세
        """
        query = urlencode(self._query({'sync': sync}))
        return self._bootpay.get(
            f'alimtalk/templates/{template_id}{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def update(self, template_id: str, params: AlimtalkTemplateUpdateParams):
        """
        자체 템플릿 수정
        PUT /v1/alimtalk/templates/{template_id}
        ⚠️ **부분 수정이 아니다.** 보내지 않은 필드는 nil 로 덮어써지므로 항상 전체 필드를 보낸다.
        ⚠️ 등록된 템플릿을 수정하면 벤더에도 수정 요청이 나간다.
           수정 가능 상태는 초안 / REG(등록) / REJ(승인반려) / KRR(등록거절) 뿐이다 — APR·REQ 는 거부된다.
        storage_image_url 을 빈 값으로 보내면 **이미지 삭제**로 처리되어 벤더에도 전달된다.
        :param template_id: 템플릿 ID
        :param params: 수정할 템플릿 정보
        :return: 수정된 템플릿
        """
        return self._bootpay.put(
            f'alimtalk/templates/{template_id}',
            self._compact(params),
            headers=self._alimtalk_headers()
        )

    def delete(self, template_id: str):
        """
        자체 템플릿 삭제
        DELETE /v1/alimtalk/templates/{template_id}
        초안(등록 전)은 대행사 거부와 무관하게 로컬에서 삭제된다.
        ⚠️ 등록분은 **대행사 삭제가 성공해야** 삭제된다 — 승인(APR) 템플릿은 카카오가 거부하므로
           500(3013)이 오고 템플릿은 남는다. 같은 코드가 대행사에 선점된 채 로컬만 사라지는 것을 막기 위함이다.
        :param template_id: 템플릿 ID
        :return: 삭제 결과
        """
        return self._bootpay.delete(
            f'alimtalk/templates/{template_id}',
            headers=self._alimtalk_headers()
        )

    def register(self, template_id: str):
        """
        초안을 대행사에 등록
        POST /v1/alimtalk/templates/{template_id}/register
        ⚠️ 대행사·카카오에 실제 등록된다. 등록 전(초안) 상태에서만 호출할 수 있다.
        :param template_id: 템플릿 ID
        :return: 등록 결과
        """
        return self._bootpay.post(
            f'alimtalk/templates/{template_id}/register',
            headers=self._alimtalk_headers()
        )

    def inspect(self, template_id: str):
        """
        검수 요청
        POST /v1/alimtalk/templates/{template_id}/inspect
        ⚠️ **카카오에 검수를 요청하며 취소할 수 없다.**
        대행사 등록이 끝난 대기(R) + REG(등록) 상태에서만 호출할 수 있다 — 초안은 먼저 register 를 부른다.
        반려(REJ/KRR)된 건은 재요청이 아니라 **수정 후 재요청**이다. 반려 사유는 응답의 comments 에 담긴다.
        :param template_id: 템플릿 ID
        :return: 검수 요청 결과
        """
        return self._bootpay.post(
            f'alimtalk/templates/{template_id}/inspect',
            headers=self._alimtalk_headers()
        )

    def export(self, params: Optional[AlimtalkTemplateExportParams] = None):
        """
        템플릿 목록 내보내기
        GET /v1/alimtalk/templates/export
        scope: private(기본, 내 채널 자체 템플릿)·official(공식 카탈로그)·all
        ⚠️ 기본 format 을 **json 으로 둔다** — 서버 기본은 csv 지만, csv 본문은 JSON 이 아니라서
           공용 get 의 파싱을 통과하지 못한다. csv 를 주면 파싱 없이 원문 문자열을 담아 돌려준다
           ({'body':, 'content_type':, 'status':}).
        1회 5,000건을 넘으면 3031 로 거부되므로 채널·상태 필터로 좁힌다.
        :param params: 내보내기 파라미터
        :return: 템플릿 목록 (format=csv 면 원문 문자열 응답)
        """
        params = dict(params or {})
        if params.get('format') is None:
            params['format'] = 'json'
        query_params = self._query(params)

        if str(query_params.get('format')) == 'csv':
            return self._bootpay.get_raw(
                'alimtalk/templates/export',
                params=query_params,
                headers=self._alimtalk_headers()
            )

        query = urlencode(query_params)
        return self._bootpay.get(
            f'alimtalk/templates/export{"?" + query if query else ""}',
            headers=self._alimtalk_headers()
        )

    def image(self, image: Any, replace_url: Optional[str] = None):
        """
        이미지형 템플릿의 원본 이미지 업로드
        POST /v1/alimtalk/templates/image
        돌려받은 image_url 을 템플릿 생성/수정의 storage_image_url 로 넘긴다.
        규격을 업로드 **전에** 서버가 검사한다 — jpg/png · 500KB 이하 · 가로 500px 이상 · 2:1.
        :param image: 파일 경로(str) 또는 이미 열린 파일 객체
        :param replace_url: 주면 업로드 성공 후에 기존 파일을 지운다
        :return: {'image_url': ...}
        """
        return self._bootpay.post_multipart_file(
            'alimtalk/templates/image',
            'image',
            image,
            data=self._compact({'replace_url': replace_url}),
            headers=self._alimtalk_headers()
        )

    def highlight_image(self, image: Any, replace_url: Optional[str] = None):
        """
        아이템리스트형의 하이라이트 썸네일 업로드
        POST /v1/alimtalk/templates/highlight_image
        ⚠️ 본문 이미지와 **규격이 다르다** — jpg/png · 500KB 이하 · 가로 **108px** 이상 · **1:1**.
           본문 이미지 endpoint 로 올리면 거부된다.
        돌려받은 image_url 은 item_highlight.storage_image_url 로 넘긴다.
        ⚠️ 썸네일을 붙이면 하이라이트 글자 한도가 줄어든다 (타이틀 30→21, 설명 19→13).
        :param image: 파일 경로(str) 또는 이미 열린 파일 객체
        :param replace_url: 주면 업로드 성공 후에 기존 파일을 지운다
        :return: {'image_url': ...}
        """
        return self._bootpay.post_multipart_file(
            'alimtalk/templates/highlight_image',
            'image',
            image,
            data=self._compact({'replace_url': replace_url}),
            headers=self._alimtalk_headers()
        )

    def _compact(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        None 값을 제거한다.
        ⚠️ False 는 남긴다 — register: False 는 "초안으로만 만든다"라서 반드시 전달되어야 한다.
        """
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
        ★Idempotency-Key 를 싣지 않는다★ 알림톡 API 는 이 헤더를 읽지 않는다.
        ★BOOTPAY-ROLE 은 항상 user★ 알림톡 스코프 키가 전부 user:alimtalk_* 다.
        """
        return {'BOOTPAY-ROLE': 'user'}
