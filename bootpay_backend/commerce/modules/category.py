from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceCategory,
    CategoryCreateParams,
    CategoryUpdateParams
)


class CategoryModule:
    """카테고리 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self):
        """
        카테고리 트리 조회
        :return: List[CommerceCategory]
        """
        return self._bootpay.get('categories')

    def detail(self, category_id: str):
        """
        카테고리 단건 조회
        :param category_id: 카테고리 ID
        :return: CommerceCategory
        """
        return self._bootpay.get(f'categories/{category_id}')

    def create(self, params: CategoryCreateParams):
        """
        카테고리 생성
        :param params: 카테고리 생성 파라미터
        :return: CommerceCategory
        """
        return self._bootpay.post('categories', params)

    def update(self, params: CategoryUpdateParams):
        """
        카테고리 수정
        :param params: 카테고리 수정 파라미터 (category_id 필수)
        :return: CommerceCategory
        """
        if not params.get('category_id'):
            raise ValueError('category_id is required')
        category_id = params['category_id']
        rest = {k: v for k, v in params.items() if k != 'category_id'}
        return self._bootpay.put(f'categories/{category_id}', rest)

    def destroy(self, category_id: str):
        """
        카테고리 삭제
        :param category_id: 카테고리 ID
        :return: None
        """
        return self._bootpay.delete(f'categories/{category_id}')
