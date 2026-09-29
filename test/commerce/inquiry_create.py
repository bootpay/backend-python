"""
Commerce API - 1:1 문의 (/v1/inquiries) 테스트

회원 모드: user_id(Bootpay 회원 _id 또는 외부 회원 ID)·login_id·user_jwt 중 하나로 회원을 정하고 본인 문의만 본다.
supervisor=True 면 몰 전체 문의 — 이때 user_id 는 작성 회원 필터(선택)다.
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


def main():
    """1:1 문의 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 회원 문의 작성 — product_id 는 이 몰의 상품, order_id 는 작성 회원의 주문이어야 한다.
        created = commerce.inquiry.create(
            login_id=LOGIN_ID,
            title='배송 문의',
            content='주문한 상품이 언제 배송되나요?'
        )
        print('=== Inquiry Create Response ===')
        print(created)

        # answered=True 답변 완료만 / False 미답변만 / 생략하면 전체
        print('\n=== Inquiry List Response ===')
        print(commerce.inquiry.list(login_id=LOGIN_ID, answered=False))

        # 운영자 모드는 몰 전체 문의를 본다.
        print('\n=== Inquiry List (supervisor) Response ===')
        print(commerce.inquiry.list(supervisor=True))

        inquiry_id = (created or {}).get('_id') or (created or {}).get('id')
        if inquiry_id:
            print('\n=== Inquiry Detail Response ===')
            print(commerce.inquiry.detail(inquiry_id, login_id=LOGIN_ID))

            # 답변이 달린 문의는 409 INQUIRY_ALREADY_ANSWERED 다.
            print('\n=== Inquiry Update Response ===')
            print(commerce.inquiry.update(inquiry_id, login_id=LOGIN_ID, content='배송 예정일만 알려주세요.'))

            # 답변 등록·수정은 supervisor 전용이다 (없으면 만들고 있으면 바꾼다).
            print('\n=== Inquiry Answer Response ===')
            print(commerce.inquiry.answer(inquiry_id, content='내일 출고 예정입니다.'))

            # 달린 답변도 함께 삭제된다.
            print('\n=== Inquiry Delete Response ===')
            print(commerce.inquiry.delete(inquiry_id, supervisor=True))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
