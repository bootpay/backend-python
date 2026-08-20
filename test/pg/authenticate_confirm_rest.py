import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend
from config import get_active_pg_config

bootpay = BootpayBackend(**get_active_pg_config())

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.confirm_authentication(
        receipt_id='6368a4f5d01c7e00241cbdf3',
        otp='641773'
    )
    print(response)
    # bootpay.cancel()
