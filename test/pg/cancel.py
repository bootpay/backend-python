import sys
import os
import uuid

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from bootpay_backend import BootpayBackend
from config import get_pg_keys, TEST_DATA

keys = get_pg_keys()
bootpay = BootpayBackend(keys['application_id'], keys['private_key'])

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.cancel_payment(
        receipt_id=TEST_DATA['receipt_id'],
        cancel_id=str(uuid.uuid4()),
        cancel_username='관리자',
        cancel_message='테스트 결제 취소'
    )
    print(response)
