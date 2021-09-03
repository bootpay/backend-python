import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay import Bootpay

bootpay = Bootpay('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

result = bootpay.get_access_token()
print(result)
if result['status'] is 200:
    print(bootpay.request_payment({
        'pg': 'kcp',
        'method': 'card',
        'order_id': str(time.time()),
        'price': 1000,
        'name': '테스트 부트페이 상품',
        'return_url': 'https://dev-api.bootpay.co.kr/callback',
        'extra': {
            'expire': 30
        }
    }))
