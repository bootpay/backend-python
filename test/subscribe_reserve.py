import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay import Bootpay

bootpay = Bootpay('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

tokenResponse = bootpay.get_access_token()
if tokenResponse['status'] == 200:
    result = bootpay.subscribe_billing_reserve(
        '612deb53019943001fb52312',
        '정기 결제 테스트 아이템',
        3000,
        '12345'
    )
    print(result)

