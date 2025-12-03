import sys
import os
import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

# bootpay = BootpayBackend('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')
bootpay = BootpayBackend('59bfc738e13f337dbd6ca48a', 'pDc0NwlkEX3aSaHTp/PPL/i8vn5E/CqRChgyEp/gHD0=', 'development')

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.cash_receipt_cancel_on_receipt(
        receipt_id='62e0f11f1fc192036b1b3c92',
    )
    print(response)
