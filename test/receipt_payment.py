import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

# bootpay = BootpayBackend("5b8f6a4d396fa665fdc2b5ea", "rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=")
bootpay = BootpayBackend("624b890f2701800021f68823", "/fZkbbIoZKxuJYIXrbA2RQWvLKBysxS+JwWenOrHRmQ=")

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.receipt_payment('634e46dbd01c7e00244d0b38')
    print(response)


