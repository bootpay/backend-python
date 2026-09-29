"""
Commerce API - 공지사항 (/v1/notices) 테스트

supervisor=True 면 운영자 모드로 요청한다 — view='all' 로 비공개 공지까지 조회할 수 있고
등록·수정·삭제는 supervisor 전용이다.
⚠️ 고객 모드는 몰 공지사항 사용여부가 꺼져 있으면 BOARD_FEATURE_DISABLED 로 거절된다.
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
    """공지사항 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        print('=== Notice List Response ===')
        print(commerce.notice.list(page=1, limit=20))

        print('\n=== Notice List (supervisor) Response ===')
        print(commerce.notice.list(keyword='점검', view='all', supervisor=True))

        # is_notice 는 상단 고정(중요 공지) 여부다.
        created = commerce.notice.create(
            title='서버 점검 안내',
            content='9월 30일 00시부터 2시간 동안 점검이 진행됩니다.',
            is_notice=True,
            is_display=True
        )
        print('\n=== Notice Create Response ===')
        print(created)

        notice_id = (created or {}).get('_id') or (created or {}).get('id')
        if notice_id:
            print('\n=== Notice Detail Response ===')
            print(commerce.notice.detail(notice_id, supervisor=True))

            print('\n=== Notice Update Response ===')
            print(commerce.notice.update(notice_id, is_display=False))

            print('\n=== Notice Delete Response ===')
            print(commerce.notice.delete(notice_id))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
