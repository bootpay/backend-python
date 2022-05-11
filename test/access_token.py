import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

bootpay = BootpayBackend('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')

result = bootpay.get_access_token()
print(result)
