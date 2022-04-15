import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay import Bootpay

bootpay = Bootpay('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.destroy_billing_key(
        billing_key='6258d04dd01c7e001b19e244',
    )
    print(response)
