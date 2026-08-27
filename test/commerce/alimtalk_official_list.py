"""
Commerce API - Alimtalk Official (부트페이 공식 알림톡 템플릿) 테스트

공식 템플릿은 부트페이가 미리 카카오 승인을 받아 둔 것이라, 그룹키가 등록된 채널이면
검수 없이 즉시 발송된다 (채널 등록 시 그룹 등록이 함께 끝나므로 따로 채택할 것이 없다).
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
    """공식 알림톡 템플릿 조회 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # keyword 는 본문·이름·분류를 부분일치(대소문자 무시)로 훑는다.
        # msg_type 은 BA(기본형)·EX(부가정보형)만 존재한다 (그룹 템플릿이라 AD/MI 는 쓸 수 없다).
        response = commerce.alimtalk_official.list({
            'keyword': '주문',
            'msg_type': 'BA',
            'page': 1,
            'per': 20
        })
        print('=== Alimtalk Official List Response ===')
        print(response)

        # 보내려는 문구로 추천받기 — 유사도 score(0~1) 내림차순
        recommend = commerce.alimtalk_official.recommend({
            'text': '주문이 접수되었습니다. 감사합니다.',
            'limit': 5
        })
        print('\n=== Alimtalk Official Recommend Response ===')
        print(recommend)

        # ksp_id 를 주면 그 채널의 변수 예문 사전으로 variable_examples 를 채워 준다 (표시용).
        detail = commerce.alimtalk_official.detail('OFFICIAL_CODE_HERE', ksp_id='KSP_ID_HERE')
        print('\n=== Alimtalk Official Detail Response ===')
        print(detail)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
