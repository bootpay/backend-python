import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

# bootpay = BootpayBackend('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')
bootpay = BootpayBackend("5b8f6a4d396fa665fdc2b5ea", "rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=")

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.request_subscribe_card_payment(
        billing_key='62b2c3cfd01c7e001cc20a84',
        order_name='테스트결제',
        order_id=str(time.time()),
        price=100,
        user={
            "phone": '01000000000',
            "username": '홍길동',
            "email": 'test@bootpay.co.kr'
        }
    )
    print(response)