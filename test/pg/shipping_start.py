import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

bootpay = BootpayBackend('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.shipping_start(
        receipt_id="62a946aad01c7e001b7dc20b",
        tracking_number='3989838',
        delivery_corp='CJ대한통운',
        user={
            "phone": '01000000000',
            "username": '홍길동',
            "address": "서울특별시 종로구",
            "zipcode": "039899"
        }
    )
    print(response)
