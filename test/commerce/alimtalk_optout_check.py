"""
Commerce API - Alimtalk Optout (알림톡 수신거부) 테스트

발송 판정과 같은 기준으로 다룬다 — 부트페이 전역(global) + 내 프로젝트.
⚠️ 전역 건은 조회는 되지만 해제할 수 없다 (releasable: False).
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
    """알림톡 수신거부 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 발송 전 사전 확인 — 벌크에서 skipped 로 낭비될 건을 미리 뺄 수 있다.
        # 1회 최대 1,000건이고 넘으면 -48 이다 (중복은 서버가 제거).
        check = commerce.alimtalk_optout.check({
            'phones': ['01012345678', '01087654321']
        })
        print('=== Alimtalk Optout Check Response ===')
        print(check)

        # 등록은 내 프로젝트 스코프로 남고 (source: api) 같은 번호를 다시 등록해도 멱등이다.
        create = commerce.alimtalk_optout.create({
            'phone': '01012345678',
            'reason': '고객 요청'
        })
        print('\n=== Alimtalk Optout Create Response ===')
        print(create)

        # phone 은 숫자만 남겨 부분일치로 찾는다 (정확 매칭이 아니다). 50건 단위 페이징.
        print('\n=== Alimtalk Optout List Response ===')
        print(commerce.alimtalk_optout.list({'phone': '0101234', 'page': 1}))

        # 해제는 내 프로젝트 스코프 건만 되고 멱등이다.
        # 전역 차단은 해제되지 않고 global_blocked: True 로 알려 준다.
        print('\n=== Alimtalk Optout Release Response ===')
        print(commerce.alimtalk_optout.release('01012345678'))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
