"""Commerce API - Mall Product (V1 products) tests."""
import pytest


class TestCommerceProductMall:
    """Commerce Mall 상품 endpoint 통합 테스트"""

    def test_products_default(self, commerce_client):
        """상품 목록 조회 (page/limit 기본 1/20)"""
        response = commerce_client.product.products()
        print(f"[Commerce] product.products = {response}")

        assert response is not None

    def test_products_with_params(self, commerce_client):
        """page/limit/sort 지정 조회"""
        response = commerce_client.product.products({'page': 1, 'limit': 5, 'sort': 'created_at'})
        print(f"[Commerce] product.products (params) = {response}")

        assert response is not None

    def test_product_detail_mall_invalid(self, commerce_client):
        """존재하지 않는 상품 Mall 상세 조회"""
        response = commerce_client.product.product_detail('nonexistent_product_id')
        print(f"[Commerce] product.product_detail (invalid) = {response}")

        assert response is not None
