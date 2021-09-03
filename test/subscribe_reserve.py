import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay import Bootpay

bootpay = Bootpay('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

result = bootpay.get_access_token()
if result['status'] is 200:
    print(bootpay.subscribe_billing_reserve(
        '5b025b33e13f33310ce56fb',
        '정기 결제 테스트 아이템',
        3000,
        '12345',
        time.time() + 10,
        'https://dev-api.bootpay.co.kr/callback')
    )
