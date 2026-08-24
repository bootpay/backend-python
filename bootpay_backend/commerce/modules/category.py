import uuid
from typing import TYPE_CHECKING, Dict, Optional

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
        POST /v1/categories
        ⚠️ 서버가 supervisor scope 를 요구한다 (scope_invalid!).
        :param params: 카테고리 생성 파라미터
        :return: CommerceCategory
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        return self._bootpay.post(
            'categories',
            params,
            headers=self._supervisor_headers(idempotency_key)
        )

    def update(self, params: CategoryUpdateParams):
        """
        카테고리 수정
        PUT /v1/categories/{category_id}
        ⚠️ 서버가 supervisor scope 를 요구한다 (scope_invalid!).
        :param params: 카테고리 수정 파라미터 (category_id 필수)
        :return: CommerceCategory
        """
        if not params.get('category_id'):
            raise ValueError('category_id is required')
        params = dict(params)
        category_id = params.pop('category_id')
        idempotency_key = params.pop('idempotency_key', None)
        return self._bootpay.put(
            f'categories/{category_id}',
            params,
            headers=self._supervisor_headers(idempotency_key)
        )

    def destroy(self, category_id: str, idempotency_key: Optional[str] = None):
        """
        카테고리 삭제
        DELETE /v1/categories/{category_id}
        ⚠️ 서버가 supervisor scope 를 요구한다 (scope_invalid!).
        :param category_id: 카테고리 ID
        :param idempotency_key: 미지정시 자동 생성
        :return: None
        """
        return self._bootpay.delete(
            f'categories/{category_id}',
            headers=self._supervisor_headers(idempotency_key)
        )

    def _supervisor_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        카테고리 쓰기(등록/수정/삭제) 요청 헤더 — 서버가 supervisor scope 를 요구한다.
        Idempotency-Key 는 미지정시 매 호출마다 생성된다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }
