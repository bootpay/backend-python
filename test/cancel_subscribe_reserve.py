import sys
import os
import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay import Bootpay

bootpay = Bootpay('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')

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
    if 'error_code' not in response:
        cancel = bootpay.cancel_subscribe_reserve(
            reserve_id=response['reserve_id']
        )
        print(cancel)
