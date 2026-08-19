import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceMallSetting,
    MallSettingUpdateParams
)


class MallSettingModule:
    """몰 설정 모듈 (supervisor scope 전용)"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def get_mall_setting(self, idempotency_key: Optional[str] = None):
        """
        몰 설정 조회
        GET /v1/mall-setting (supervisor scope 토큰 전용)
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceMallSetting
        """
        return self._bootpay.get('mall-setting', headers=self._supervisor_headers(idempotency_key))

    def detail(self, idempotency_key: Optional[str] = None):
        """get_mall_setting 별칭"""
        return self.get_mall_setting(idempotency_key)

    def update_mall_setting(self, params: MallSettingUpdateParams, idempotency_key: Optional[str] = None):
        """
        몰 설정 수정
        PUT /v1/mall-setting (supervisor scope 토큰 전용)
        요청 바디는 flatten 형식이며 전달된 값(non-None)만 서버로 전송된다.
        :param params: 수정할 설정값
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceMallSetting
        """
        return self._bootpay.put(
            'mall-setting',
            self._compact(params),
            headers=self._supervisor_headers(idempotency_key)
        )

    def update(self, params: MallSettingUpdateParams, idempotency_key: Optional[str] = None):
        """update_mall_setting 별칭"""
        return self.update_mall_setting(params, idempotency_key)

    def _compact(self, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """None 값을 제거한다."""
        return {k: v for k, v in (params or {}).items() if v is not None}

    def _supervisor_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        supervisor 전용 요청 헤더
        Idempotency-Key 는 미지정시 매 호출마다 생성된다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }
