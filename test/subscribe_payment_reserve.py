import sys
import os
import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

bootpay = BootpayBackend("5b8f6a4d396fa665fdc2b5ea", "rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=")

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
        reserve_execute_at=(datetime.datetime.now() + datetime.timedelta(seconds=5)).astimezone().strftime(
            '%Y-%m-%dT%H:%M:%S%z')
    )
    print(response)
