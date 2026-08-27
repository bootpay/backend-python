"""
Commerce API - Alimtalk Sender Create (알림톡 발신프로필 등록) 테스트

⚠️ otp 는 채널 관리자 휴대폰으로 문자를 실제 발송하고, create 는 카카오에 발신프로필을 실제 등록한다.
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
    """알림톡 발신프로필 등록 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 1. 카카오 카테고리 조회 — 등록에 필요한 category_code 후보다.
        categories = commerce.alimtalk_sender.categories()
        print('=== Alimtalk Categories Response ===')
        print(categories)

        # 2. 채널 관리자폰으로 OTP 발송 (실제로 문자가 나간다)
        otp_response = commerce.alimtalk_sender.otp({
            'yellow_id': '@부트페이',
            'phone': '01012345678'
        })
        print('\n=== Alimtalk Sender OTP Response ===')
        print(otp_response)

        # 3. 발신프로필 등록 — 성공하면 서버가 그룹키 등록까지 수행하므로
        #    공식 템플릿은 별도 채택 없이 바로 발송할 수 있다.
        create_response = commerce.alimtalk_sender.create({
            'otp': '123456',
            'yellow_id': '@부트페이',
            'phone': '01012345678',
            'category_code': 'CATEGORY_CODE_HERE'
        })
        print('\n=== Alimtalk Sender Create Response ===')
        print(create_response)

        # 4. 연동 채널 목록 / 상세 (sync=True 면 벤더에서 상태를 다시 읽는다 — 느리다)
        print('\n=== Alimtalk Sender List Response ===')
        print(commerce.alimtalk_sender.list())
        print('\n=== Alimtalk Sender Detail Response ===')
        print(commerce.alimtalk_sender.detail('KSP_ID_HERE', sync=True))

        # 5. 변수 예문 사전 — 미리보기 표시용이며 발송값이 아니다 (보낸 키만 덮어쓴다).
        print('\n=== Alimtalk Sender Variable Examples Response ===')
        print(commerce.alimtalk_sender.variable_examples('KSP_ID_HERE', {
            'user_name': '홍길동',
            'company_name': '부트페이몰'
        }))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
