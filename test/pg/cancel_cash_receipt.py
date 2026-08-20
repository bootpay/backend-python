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
    response = bootpay.cancel_cash_receipt(
        receipt_id='62f20fc21fc192036b4f6f89',
        cancel_username='시스템',
        cancel_message='테스트'
    )
    print(response)
