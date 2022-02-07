import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from bootpay import Bootpay

bootpay = Bootpay('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

tokenResponse = bootpay.get_access_token()
if tokenResponse['status'] == 200:
    result = bootpay.cancel('1234', 'test', 'test결제 취소')
    print(result)
    # bootpay.cancel()
