import sys
import os
import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend
from config import get_active_pg_config

bootpay = BootpayBackend(**get_active_pg_config())

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.subscribe_payment_reserve(
        billing_key='[ 빌링키 ]',
        order_name='테스트결제',
        order_id=str(time.time()),
        price=1000,
        user={
            "phone": '01000000000',
            "username": '홍길동',
            "email": 'test@bootpay.co.kr'
        },
        metadata={
            "test1": 1234,
            "test2": 5678,
        },
        reserve_execute_at=(datetime.datetime.now() + datetime.timedelta(seconds=5)).astimezone().strftime(
            '%Y-%m-%dT%H:%M:%S%z')
    )
    print(response)
