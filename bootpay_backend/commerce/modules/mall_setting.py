import uuid
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import MallSettingUpdateParams


class MallSettingModule:
    """몰 설정 모듈 (supervisor scope 토큰 전용)"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def _supervisor_headers(self, idempotency_key: Optional[str] = None):
        """supervisor 전용 헤더 생성"""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }

    def get_mall_setting(self, idempotency_key: Optional[str] = None):
        """
        몰 설정 조회 (GET /v1/mall-setting)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 몰 설정 정보
        """
        return self._bootpay.get('mall-setting', headers=self._supervisor_headers(idempotency_key))

    def detail(self, idempotency_key: Optional[str] = None):
        return self.get_mall_setting(idempotency_key)

    def update_mall_setting(self, params: MallSettingUpdateParams, idempotency_key: Optional[str] = None):
        """
        몰 설정 수정 (PUT /v1/mall-setting)
        요청 바디는 flatten 형식이며 전달된 값(None이 아닌 값)만 서버로 전송된다.
        :param params: 수정 파라미터
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 몰 설정 정보
        """
        payload = {key: value for key, value in (params or {}).items() if value is not None}
        return self._bootpay.put(
            'mall-setting',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def update(self, params: MallSettingUpdateParams, idempotency_key: Optional[str] = None):
        return self.update_mall_setting(params, idempotency_key)
