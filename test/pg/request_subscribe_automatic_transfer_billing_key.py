import sys
import os
import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

bootpay = BootpayBackend("5b8f6a4d396fa665fdc2b5ea", "rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=")

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.request_subscribe_automatic_transfer_billing_key(
        pg="나이스페이",
        order_name='테스트결제',
        subscription_id=str(time.time()),
        price=1000,
        username='홍길동',
        bank_name='국민',
        bank_account='67560123412342472',
        identity_no='901014',
        cash_receipt_identity_no='01012341234',
        phone='01012341234'
    )
    # {'receipt_id': '66542d4be86c1eedf6b17965', 'order_id': '1716792650.95292', 'price': 1000, 'tax_free': 0, 'cancelled_price': 0, 'cancelled_tax_free': 0, 'order_name': '테스트결제', 'company_name': '윤태섭', 'gateway_url': 'https://gw.bootpay.co.kr', 'metadata': {}, 'sandbox': True, 'pg': '나이스페이먼츠', 'method': '계좌자동이체', 'method_symbol': 'automatic_traorigin': '계좌자동이체', 'method_origin_symbol': 'automatic_transfer_rest', 'requested_at': '2024-05-27T15:50:51+09:00', 'status_locale': '자동결제빌링키발급이전', 'currency': 'KRW', 'status': 41}
    print(response)
