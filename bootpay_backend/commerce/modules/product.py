from typing import TYPE_CHECKING, Optional, List
from urllib.parse import urlencode
import os
import json

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceProduct,
    ProductListParams,
    ProductStatusParams
)


class ProductModule:
    """상품 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def list(self, params: Optional[ProductListParams] = None):
        """
        상품 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceProduct], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']
            if params.get('type') is not None:
                query_params['type'] = params['type']
            if params.get('period_type'):
                query_params['period_type'] = params['period_type']
            if params.get('s_at'):
                query_params['s_at'] = params['s_at']
            if params.get('e_at'):
                query_params['e_at'] = params['e_at']
            if params.get('category_code'):
                query_params['category_code'] = params['category_code']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'products{"?" + query if query else ""}')

    def create(self, product: CommerceProduct, image_paths: Optional[List[str]] = None):
        """
        상품 생성 (이미지 포함)
        :param product: 상품 정보
        :param image_paths: 이미지 파일 경로 배열
        :return: CommerceProduct
        """
        return self._bootpay.post_multipart('products', product, image_paths)

    def detail(self, product_id: str):
        """
        상품 상세 조회
        :param product_id: 상품 ID
        :return: CommerceProduct
        """
        return self._bootpay.get(f'products/{product_id}')

    def update(self, product: CommerceProduct):
        """
        상품 수정
        :param product: 상품 정보
        :return: CommerceProduct
        """
        if not product.get('product_id'):
            raise ValueError('product_id is required')
        return self._bootpay.put(f'products/{product["product_id"]}', product)

    def status(self, params: ProductStatusParams):
        """
        상품 상태 변경
        :param params: 상태 변경 파라미터
        :return: CommerceProduct
        """
        if not params.get('product_id'):
            raise ValueError('product_id is required')
        return self._bootpay.put(f'products/{params["product_id"]}/status', params)

    def delete(self, product_id: str):
        """
        상품 삭제
        :param product_id: 상품 ID
        :return: None
        """
        return self._bootpay.delete(f'products/{product_id}')
