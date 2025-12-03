import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from bootpay_backend import BootpayBackend
from config import get_pg_keys, TEST_DATA

keys = get_pg_keys()
bootpay = BootpayBackend(keys['application_id'], keys['private_key'])

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.destroy_billing_key(
        billing_key=TEST_DATA['billing_key'],
    )
    print(response)
