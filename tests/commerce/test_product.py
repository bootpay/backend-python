"""Commerce API - Product tests."""
import pytest


class TestCommerceProduct:
    """Commerce Product 모듈 통합 테스트"""

    def test_product_list(self, commerce_client):
        """상품 목록 조회"""
        response = commerce_client.product.list({'page': 1, 'limit': 10})
        print(f"[Commerce] product.list = {response}")

        assert response is not None

    def test_product_list_with_keyword(self, commerce_client):
        """키워드로 상품 검색"""
        response = commerce_client.product.list({
            'page': 1,
            'limit': 5,
            'keyword': 'test',
        })
        print(f"[Commerce] product.list (keyword) = {response}")

        assert response is not None

    def test_product_detail_invalid(self, commerce_client):
        """존재하지 않는 상품 상세 조회"""
        response = commerce_client.product.detail(product_id='nonexistent_product_id')
        print(f"[Commerce] product.detail (invalid) = {response}")

        assert response is not None

    def test_product_create_and_delete(self, commerce_client):
        """상품 생성 후 삭제 (생성/삭제 순환 테스트)"""
        product_data = {
            'name': '통합테스트 상품',
            'price': 10000,
            'type': 1,
        }

        # 상품 생성
        create_response = commerce_client.product.create(product_data)
        print(f"[Commerce] product.create = {create_response}")
        assert create_response is not None

        # 생성 성공 시 삭제까지 수행
        product_id = create_response.get('product_id')
        if product_id:
            delete_response = commerce_client.product.delete(product_id=product_id)
            print(f"[Commerce] product.delete = {delete_response}")

    def test_product_update_invalid(self, commerce_client):
        """존재하지 않는 상품 수정"""
        try:
            response = commerce_client.product.update({
                'product_id': 'nonexistent_product_id',
                'name': '수정 테스트',
            })
            print(f"[Commerce] product.update (invalid) = {response}")
            assert response is not None
        except ValueError:
            # product_id 누락 시 ValueError 발생 가능
            pass

    def test_product_status_invalid(self, commerce_client):
        """존재하지 않는 상품 상태 변경"""
        try:
            response = commerce_client.product.status({
                'product_id': 'nonexistent_product_id',
                'status': 1,
            })
            print(f"[Commerce] product.status (invalid) = {response}")
            assert response is not None
        except ValueError:
            pass
