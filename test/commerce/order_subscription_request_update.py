"""
Commerce API - 정기구독 변경요청 승인/반려 테스트
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
    """정기구독 변경요청 승인/반려 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # approval: 'approve'(승인) | 'reject'(반려)
        response = commerce.order_subscription_request.update({
            'request_history_id': 'REQUEST_HISTORY_ID_HERE',
            'approval': 'approve',
            'reason': '승인 사유'
        })
        print('=== OrderSubscriptionRequest Update Response ===')
        print(response)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
