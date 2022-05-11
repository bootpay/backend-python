import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from bootpay_backend import BootpayBackend

bootpay = BootpayBackend('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

result = bootpay.get_access_token()
if result['status'] == 200:
    print(bootpay.cancel('1234', 'test', 'test결제 취소'))
    # bootpay.cancel()
