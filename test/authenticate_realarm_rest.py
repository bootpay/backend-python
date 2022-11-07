import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

bootpay = BootpayBackend('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.realarm_authentication(
        receipt_id='6368a51dd01c7e002a1cbe21'
    )
    print(response)
    # bootpay.cancel()