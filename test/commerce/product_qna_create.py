"""
Commerce API - 상품문의 (/v1/product-qnas) 테스트

회원(user_id·login_id·user_jwt) 또는 비회원(guest_name + guest_password, 몰이 비회원 작성을 허용할 때) 작성을 받는다.
고객 모드 목록은 product_id 가 필수이고, supervisor=True + view='all' 이면 몰 전체(숨김 포함)다.
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

PRODUCT_ID = 'PRODUCT_ID'


def main():
    """상품문의 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 비회원 작성 — guest_name + guest_password 가 함께 필요하다.
        created = commerce.product_qna.create(
            product_id=PRODUCT_ID,
            title='재입고 문의',
            content='품절된 색상 재입고 예정이 있나요?',
            is_secret=True,
            guest_name='비회원',
            guest_password='1234'
        )
        print('=== ProductQna Create Response ===')
        print(created)

        # 다른 사람의 비밀글은 is_viewable: False 로 본문 없이 온다.
        print('\n=== ProductQna List Response ===')
        print(commerce.product_qna.list(product_id=PRODUCT_ID))

        # 운영자 모드 + view='all' 이면 숨김 글까지 몰 전체를 본다.
        print('\n=== ProductQna List (supervisor) Response ===')
        print(commerce.product_qna.list(view='all', supervisor=True))

        product_qna_id = (created or {}).get('_id') or (created or {}).get('id')
        if product_qna_id:
            print('\n=== ProductQna Detail Response ===')
            print(commerce.product_qna.detail(product_qna_id, supervisor=True))

            # 답변이 달린 문의는 409 PRODUCT_QNA_ALREADY_ANSWERED,
            # 비회원 비밀번호가 틀리면 403 PRODUCT_QNA_GUEST_PASSWORD_INVALID 다.
            print('\n=== ProductQna Update Response ===')
            print(commerce.product_qna.update(product_qna_id, content='블랙 색상 재입고 문의드립니다.',
                                              guest_password='1234'))

            # 답변 등록·수정은 supervisor 전용이다.
            print('\n=== ProductQna Answer Response ===')
            print(commerce.product_qna.answer(product_qna_id, content='다음 주 중 입고 예정입니다.'))

            # guest_password 는 URL 쿼리가 아닌 본문으로 나간다.
            print('\n=== ProductQna Delete Response ===')
            print(commerce.product_qna.delete(product_qna_id, guest_password='1234'))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
