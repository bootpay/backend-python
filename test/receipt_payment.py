import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

bootpay = BootpayBackend('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.receipt_payment('61b009aaec81b4057e7f6ecd')
    print(response)