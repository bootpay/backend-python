import sys
import os
import uuid 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from bootpay_backend import BootpayBackend

bootpay = BootpayBackend('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.cancel_payment(
        receipt_id='62ba5a3cd01c7e001fb45c46', 
        cancel_id=str(uuid.uuid4()),
        cancel_username='test', 
        cancel_message='test결제 취소'
    )
    print(response)
    # bootpay.cancel()
