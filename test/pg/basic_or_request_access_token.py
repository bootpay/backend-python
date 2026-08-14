import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from bootpay_backend import BootpayBackend
from config import get_pg_keys

# client key / secret key 기반 Basic 인증용 키
CLIENT_KEY = 'CLIENT_KEY_HERE'
SECRET_KEY = 'SECRET_KEY_HERE'

keys = get_pg_keys()

# 1. application_id / private_key 사용시 (토큰 발급 요청)
bootpay = BootpayBackend(keys['application_id'], keys['private_key'])
print(bootpay.basic_or_request_access_token())

# 2. client_key 지정시 (토큰 발급 없이 Basic 인증으로 요청)
basic_bootpay = BootpayBackend(
    keys['application_id'],
    keys['private_key'],
    client_key=CLIENT_KEY,
    secret_key=SECRET_KEY
)
response = basic_bootpay.basic_or_request_access_token()
if response.get('success'):
    # 토큰 발급 없이 Basic 인증으로 결제건 조회
    print(basic_bootpay.receipt_payment('62b2c3c2d01c7e001bc20b10'))
