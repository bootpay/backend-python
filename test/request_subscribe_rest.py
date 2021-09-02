import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import bootpay

api = bootpay.Api('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

result = api.get_access_token()
if result['status'] is 200:
    response = api.get_subscribe_billing_key(
        'nicepay',
        str(time.time()),
        '30일 결제권',
        '[ 카드 번호 ]',
        '[ 카드 비밀번호 앞자리 2개 ]',
        '[ 카드 만료 연도 2자리 ]',
        '[ 카드 만료 월 2자리 ]',
        '[ 카드 소유주 생년월일 혹은 사업자 등록번호 ]',
        None,
        {
            'subscribe_test_payment': 1
        }
    )
    print(response)

    # Billing key를 취소할 때 쓰는 API
    print(
        api.destroy_subscribe_billing_key(result['data']['billing_key'])
    )
