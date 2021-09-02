import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import bootpay

api = bootpay.Api('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

result = api.get_access_token()
if result['status'] is 200:
    print(api.certificate('1234'))
