import uuid
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource


class StoreModule:
    """스토어 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def _store_headers(self, idempotency_key: Optional[str] = None):
        """스토어 조회 전용 헤더 생성"""
        return {'Idempotency-Key': idempotency_key or str(uuid.uuid4())}

    def get_store(self, idempotency_key: Optional[str] = None):
        """
        가맹점 기본 정보 조회 (/v1/store)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 가맹점 기본 정보
        """
        return self._bootpay.get('store', headers=self._store_headers(idempotency_key))

    def info(self, idempotency_key: Optional[str] = None):
        return self.get_store(idempotency_key)

    def get_store_detail(self, idempotency_key: Optional[str] = None):
        """
        가맹점 상세 정보 조회 (/v1/store/detail)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 가맹점 상세 정보
        """
        return self._bootpay.get('store/detail', headers=self._store_headers(idempotency_key))

    def detail(self, idempotency_key: Optional[str] = None):
        return self.get_store_detail(idempotency_key)
