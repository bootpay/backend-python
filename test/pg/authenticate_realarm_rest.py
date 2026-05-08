import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend
from config import get_active_pg_config

bootpay = BootpayBackend(**get_active_pg_config())

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.realarm_authentication(
        receipt_id='6368a51dd01c7e002a1cbe21'
    )
    print(response)
    # bootpay.cancel()
