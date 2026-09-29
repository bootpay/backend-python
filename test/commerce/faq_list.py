"""
Commerce API - FAQ (/v1/faqs) 테스트

supervisor=True 면 운영자 모드로 요청한다 — view='all' 로 비공개 FAQ 까지 조회할 수 있고
등록·수정·삭제는 supervisor 전용이다.
⚠️ 고객 모드는 몰 FAQ 사용여부가 꺼져 있으면 BOARD_FEATURE_DISABLED 로 거절된다.
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


def main():
    """FAQ 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 고객 모드 목록 — 공개 FAQ 만 보인다.
        print('=== FAQ List Response ===')
        print(commerce.faq.list(page=1, limit=20))

        # 운영자 모드 — view='all' 이면 비공개 FAQ 까지 보인다.
        print('\n=== FAQ List (supervisor) Response ===')
        print(commerce.faq.list(view='all', supervisor=True))

        # 등록·수정·삭제는 supervisor 전용이다.
        created = commerce.faq.create(
            title='배송은 얼마나 걸리나요?',
            content='결제 후 2~3일 내에 출고됩니다.',
            is_display=True
        )
        print('\n=== FAQ Create Response ===')
        print(created)

        faq_id = (created or {}).get('_id') or (created or {}).get('id')
        if faq_id:
            print('\n=== FAQ Detail Response ===')
            print(commerce.faq.detail(faq_id, supervisor=True))

            # 보낸 필드만 바뀐다. images 는 보내면 목록 전체를 교체한다 ([] 면 모두 삭제).
            print('\n=== FAQ Update Response ===')
            print(commerce.faq.update(faq_id, content='결제 후 1~2일 내에 출고됩니다.'))

            print('\n=== FAQ Delete Response ===')
            print(commerce.faq.delete(faq_id))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
