import uuid
from typing import TYPE_CHECKING, Optional, List, Dict, Any
from urllib.parse import urlencode
import os
import json

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceProduct,
    ProductListParams,
    MallProductListParams,
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

    def products(self, params: Optional[MallProductListParams] = None):
        """
        상품 목록 조회 (V1 Mall API)
        GET /v1/products
        page/limit 은 미지정시 각각 1 / 20 이 적용되고, 나머지 값은 지정된 것만 전송한다.
        ⚠️ keyword 는 서버(v1/products_controller#index)가 읽지 않는다 — page/limit/category_id/ex_uid/sort 만 사용하며
           keyword 를 보내도 조용히 무시된다. 하위호환 때문에 인자는 남겨두되, 검색이 필요하면 서버 지원이 선행되어야 한다.
        :param params: 조회 파라미터
        :return: {'items': List[CommerceProduct], 'total': int}
        """
        params = dict(params or {})
        user_jwt = params.pop('user_jwt', None)
        idempotency_key = params.pop('idempotency_key', None)

        query_params = {
            'page': 1 if params.get('page') is None else params['page'],
            'limit': 20 if params.get('limit') is None else params['limit'],
        }
        if params.get('category_id'):
            query_params['category_id'] = params['category_id']
        if params.get('sort'):
            query_params['sort'] = params['sort']
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

        return self._bootpay.get(
            f'products?{urlencode(query_params)}',
            headers=self._mall_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def create(self, product: CommerceProduct, image_paths: Optional[List[str]] = None,
               idempotency_key: Optional[str] = None):
        """
        상품 생성
        POST /v1/products
        image_paths 가 있으면 multipart/form-data, 없으면 JSON 으로 보낸다.
        :param product: 상품 정보 (여기 명시되지 않은 값도 서버 _product_params 로 그대로 전달된다)
        :param image_paths: 이미지 파일 경로 배열
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceProduct
        """
        payload = self._compact(product)
        headers = self._manager_headers(idempotency_key)

        if not image_paths:
            return self._bootpay.post('products', payload, headers=headers)

        return self._bootpay.post_multipart('products', payload, image_paths, headers=headers)

    def detail(self, product_id: str):
        """
        상품 상세 조회
        :param product_id: 상품 ID
        :return: CommerceProduct
        """
        return self._bootpay.get(f'products/{product_id}')

    def product_detail(self, product_id: str, user_jwt: Optional[str] = None,
                       idempotency_key: Optional[str] = None):
        """
        상품 상세 조회 (V1 Mall API)
        GET /v1/products/{product_id}
        :param product_id: 상품 ID
        :param user_jwt: 회원 JWT (선택)
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceProduct
        """
        return self._bootpay.get(
            f'products/{product_id}',
            headers=self._mall_headers(user_jwt=user_jwt, idempotency_key=idempotency_key)
        )

    def lookup_product(self, product_id: str, idempotency_key: Optional[str] = None):
        """
        상품 정보 조회 — `product_detail` 과 같은 endpoint 다.
        ruby 동기화 파이프라인이 쓰는 이름이라 호환용으로 둔다.
        :param product_id: 상품 ID
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceProduct
        """
        return self.product_detail(product_id, idempotency_key=idempotency_key)

    def update(self, product: CommerceProduct, idempotency_key: Optional[str] = None):
        """
        상품 수정
        PUT /v1/products/{product_id}
        바뀐 값만 보내면 된다. ⚠️ category_id 는 키 존재 여부로 '해제 의사'를 판별하므로 주의.
        :param product: 상품 정보
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceProduct
        """
        if not product.get('product_id'):
            raise ValueError('product_id is required')
        return self._bootpay.put(
            f'products/{product["product_id"]}',
            self._compact(product),
            headers=self._manager_headers(idempotency_key)
        )

    def status(self, params: ProductStatusParams):
        """
        상품 판매/노출 상태 변경
        PUT /v1/products/{product_id}/status
        ⚠️ 재고(stock)는 여기가 아니라 update 로 바꾼다.
        :param params: 상태 변경 파라미터
        :return: CommerceProduct
        """
        if not params.get('product_id'):
            raise ValueError('product_id is required')
        params = dict(params)
        product_id = params.pop('product_id')
        idempotency_key = params.pop('idempotency_key', None)
        return self._bootpay.put(
            f'products/{product_id}/status',
            self._compact(params),
            headers=self._manager_headers(idempotency_key)
        )

    def delete(self, product_id: str, idempotency_key: Optional[str] = None):
        """
        상품 삭제
        DELETE /v1/products/{product_id}
        :param product_id: 상품 ID
        :param idempotency_key: 미지정시 자동 생성
        :return: None
        """
        return self._bootpay.delete(
            f'products/{product_id}',
            headers=self._manager_headers(idempotency_key)
        )

    def _compact(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """None 값을 제거한다."""
        return {k: v for k, v in dict(payload or {}).items() if v is not None}

    def _manager_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        상품 쓰기(등록/수정/삭제/상태변경) 요청 헤더
        서버가 manager scope 를 요구한다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'manager'
        }

    def _mall_headers(self, user_jwt: Optional[str] = None, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        V1 Mall API 요청 헤더
        Idempotency-Key 는 미지정시 매 호출마다 생성되고, Bootpay-User-JWT 는 값이 있을 때만 붙는다.
        """
        headers = {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4())
        }
        if user_jwt:
            headers['Bootpay-User-JWT'] = user_jwt
        return headers
