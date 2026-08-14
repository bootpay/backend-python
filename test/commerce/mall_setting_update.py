"""
Commerce API - MallSetting Update (몰 설정 수정) 테스트
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
    """몰 설정 수정 테스트 (supervisor scope 토큰 전용)"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        response = commerce.mall_setting.update_mall_setting({
            'name': '부트페이 테스트 몰',
            'description': '부트페이 SDK 테스트로 갱신된 몰 설명',
            'use_notice': True,
            'use_qna': True,
            'use_faq': True,
            'customer_service_center_operation_time': {
                'mon': {'use': True, 'start_hour': 9, 'start_minute': 0, 'end_hour': 18, 'end_minute': 0},
                'tue': {'use': True, 'start_hour': 9, 'start_minute': 0, 'end_hour': 18, 'end_minute': 0},
                'wed': {'use': True, 'start_hour': 9, 'start_minute': 0, 'end_hour': 18, 'end_minute': 0},
                'thu': {'use': True, 'start_hour': 9, 'start_minute': 0, 'end_hour': 18, 'end_minute': 0},
                'fri': {'use': True, 'start_hour': 9, 'start_minute': 0, 'end_hour': 18, 'end_minute': 0},
                'sat': {'use': False, 'start_hour': 0, 'start_minute': 0, 'end_hour': 0, 'end_minute': 0},
                'sun': {'use': False, 'start_hour': 0, 'start_minute': 0, 'end_hour': 0, 'end_minute': 0}
            }
        })
        print('=== MallSetting Update Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
