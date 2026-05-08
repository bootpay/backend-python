import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend
from config import get_active_pg_config

bootpay = BootpayBackend(**get_active_pg_config())

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.request_authentication(
        pg='다날',
        method='본인인증',
        username='[ 사용자 명 ]',
        identity_no='[ 생년월일 + 주민등록번호 뒷 1자리 ]',
        carrier='[ 통신사 ]',
        phone='[ 인증 전화번호 ]',
        site_url='https://www.bootpay.co.kr',
        order_name='회원 본인인증',
        authentication_id=str(time.time())
    )
    print(response)
    # bootpay.cancel()
