import sys
import os
import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

# bootpay = BootpayBackend('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')
bootpay = BootpayBackend('59bfc738e13f337dbd6ca48a', 'pDc0NwlkEX3aSaHTp/PPL/i8vn5E/CqRChgyEp/gHD0=', 'development')

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.request_cash_receipt(
        pg='토스',
        price=1000,
        order_name='테스트',
        cash_receipt_type='소득공제',
        user={
            "username": '부트페이',
            "phone": '01000000000',
            "email": "bootpay@bootpay.co.kr"
        },
        identity_no='01000000000',
        purchased_at=datetime.datetime.now().astimezone().strftime(
            '%Y-%m-%dT%H:%M:%S%z'),
        order_id=str(time.time())
    )
    # 62f20fc21fc192036b4f6f89
    print(response)
