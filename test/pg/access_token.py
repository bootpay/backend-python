import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from bootpay_backend import BootpayBackend
from config import get_pg_keys

keys = get_pg_keys()
bootpay = BootpayBackend(keys['application_id'], keys['private_key'])

result = bootpay.get_access_token()
print(result)
