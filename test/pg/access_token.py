import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from bootpay_backend import BootpayBackend
from config import get_active_pg_config

bootpay = BootpayBackend(**get_active_pg_config())

result = bootpay.get_access_token()
print(result)
