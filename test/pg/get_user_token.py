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
    response = bootpay.request_user_token(
        user_id=TEST_DATA['user_id'],
        phone='01012345678'
    )
    print(response)
