import sys
import os
import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from bootpay_backend import BootpayBackend
from config import get_pg_keys, TEST_DATA

keys = get_pg_keys()
bootpay = BootpayBackend(keys['application_id'], keys['private_key'])

token = bootpay.get_access_token()
if 'error_code' not in token:
    # 예약 결제 등록 -> 조회 -> 취소 테스트
    response = bootpay.subscribe_payment_reserve(
        billing_key=TEST_DATA['billing_key'],
        order_name='테스트결제',
        order_id=str(time.time()),
        price=1000,
        user={
            "phone": '01000000000',
            "username": '홍길동',
            "email": 'test@bootpay.co.kr'
        },
        reserve_execute_at=(datetime.datetime.now() + datetime.timedelta(seconds=60)).astimezone().strftime(
            '%Y-%m-%dT%H:%M:%S%z')
    )
    print(response)
    if 'error_code' not in response:
        lookup = bootpay.subscribe_payment_reserve_lookup(response['reserve_id'])
        print(lookup)
        cancel = bootpay.cancel_subscribe_reserve(
            reserve_id=response['reserve_id']
        )
        print(cancel)
