import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay import Bootpay

bootpay = Bootpay('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')

response = bootpay.receipt_payment('61b009aaec81b4057e7f6ecd')
print(response)
