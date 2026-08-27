"""
Commerce API - Alimtalk Send (알림톡 발송) 테스트

⚠️ 실제로 카카오톡이 발송되고 과금된다. 샌드박스가 없다.
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
    """알림톡 발송 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # ref_id 는 멱등 키다 — 같은 (프로젝트, ref_id) 로 재요청하면 기존 receipt 를 그대로 돌려준다.
        # fallback 은 미지정(None)과 False 가 다르다: None 은 프로젝트 기본값, False 는 명시적으로 끈다.
        response = commerce.alimtalk_send.send({
            'template_code': 'TEMPLATE_CODE_HERE',
            'to': '01012345678',
            'variables': {
                'company_name': '부트페이몰',
                'user_name': '홍길동'
            },
            'ref_id': 'order-20260827-0001',
            'fallback': False
        })
        print('=== Alimtalk Send Response ===')
        print(response)

        # 벌크 발송 — 수신자 수만큼 실제 발송되고 과금된다.
        # 쿼터를 넘으면 요청 시점에 전체 거부되고(3022), 수신거부 번호는 skipped 로 과금되지 않는다.
        bulk_response = commerce.alimtalk_send.bulk({
            'template_code': 'TEMPLATE_CODE_HERE',
            'recipients': [
                {'to': '01012345678', 'ref_id': 'bulk-0001', 'variables': {'user_name': '홍길동'}},
                {'to': '01087654321', 'ref_id': 'bulk-0002', 'variables': {'user_name': '김철수'}}
            ]
        })
        print('\n=== Alimtalk Send Bulk Response ===')
        print(bulk_response)

        # 예약 취소는 접수(READY) 상태의 예약 건만 가능하다 (전송에 들어갔으면 3023).
        cancel_response = commerce.alimtalk_send.cancel('RECEIPT_ID_HERE')
        print('\n=== Alimtalk Send Cancel Response ===')
        print(cancel_response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
