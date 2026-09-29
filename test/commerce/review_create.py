"""
Commerce API - 상품평 (/v1/reviews) 테스트

회원 모드: user_id·login_id·user_jwt 로 정한 회원이 쓴 상품평만 본다.
supervisor=True 면 몰 전체 상품평 — 이때 user_id 는 작성 회원 필터(선택)다.
⚠️ 상품 상세의 공개 상품평 목록은 기존 GET /v1/products/{product_id}/reviews 를 쓴다.
"""

import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from config import get_commerce_keys

# 환경에 맞는 키 가져오기
keys = get_commerce_keys()
CLIENT_KEY = keys['client_key']
SECRET_KEY = keys['secret_key']
MODE = keys['mode']

LOGIN_ID = 'LOGIN_ID'
ORDER_ID = 'ORDER_ID'
PRODUCT_ID = 'PRODUCT_ID'


def main():
    """상품평 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # order_id 는 회원의 구매확정 주문, product_id 는 그 주문에 담긴 상품이어야 한다.
        # images 는 사진 URL 최대 5개다 (파일 업로드는 지원하지 않는다).
        created = commerce.product_review.create(
            login_id=LOGIN_ID,
            order_id=ORDER_ID,
            product_id=PRODUCT_ID,
            rating=5,
            content='사이즈도 잘 맞고 배송도 빨라서 만족합니다.',
            images=['https://cdn.example.com/review/1.jpg']
        )
        print('=== Review Create Response ===')
        print(created)

        print('\n=== Review List Response ===')
        print(commerce.product_review.list(login_id=LOGIN_ID))

        print('\n=== Review List (supervisor) Response ===')
        print(commerce.product_review.list(product_id=PRODUCT_ID, view='all', supervisor=True))

        product_review_id = (created or {}).get('_id') or (created or {}).get('id')
        if product_review_id:
            print('\n=== Review Detail Response ===')
            print(commerce.product_review.detail(product_review_id, login_id=LOGIN_ID))

            # images 는 통째로 교체한다 ([] 면 모두 삭제). 작성 후 7일이 지나면 REVIEW_EDIT_TIME_EXPIRED 다.
            print('\n=== Review Update Response ===')
            print(commerce.product_review.update(product_review_id, login_id=LOGIN_ID, rating=4, images=[]))

            # 판매자 답글(10자 이상) 등록·수정은 supervisor 전용이다.
            print('\n=== Review Reply Response ===')
            print(commerce.product_review.reply(product_review_id, content='소중한 후기 감사합니다.'))

            # 지급된 적립금 회수·상품 통계 차감이 함께 일어난다.
            print('\n=== Review Delete Response ===')
            print(commerce.product_review.delete(product_review_id, reason='광고성 후기', supervisor=True))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
