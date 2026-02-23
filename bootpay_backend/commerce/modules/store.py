from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource


class StoreModule:
    """스토어 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def get_store(self):
        """가맹점 기본 정보 조회 (/v1/store)"""
        return self._bootpay.get('store')

    def info(self):
        return self.get_store()

    def get_store_detail(self):
        """가맹점 상세 정보 조회 (/v1/store/detail)"""
        return self._bootpay.get('store/detail')

    def detail(self):
        return self.get_store_detail()
