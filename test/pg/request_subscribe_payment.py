import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend
from config import get_active_pg_config

bootpay = BootpayBackend(**get_active_pg_config())

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.request_subscribe_payment(
        billing_key='66542dfb4d18d5fc7b43e1b6',
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
