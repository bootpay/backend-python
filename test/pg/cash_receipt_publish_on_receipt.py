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
    response = bootpay.cash_receipt_publish_on_receipt(
        receipt_id='62e0f11f1fc192036b1b3c92',
        username='테스트',
        email='test@bootpay.co.kr',
        phone='01000000000',
        identity_no='01000000000',
        cash_receipt_type='소득공제'
    )
    print(response)

