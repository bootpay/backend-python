import sys
import os
import datetime
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

bootpay = BootpayBackend("5b8f6a4d396fa665fdc2b5ea", "rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=")

token = bootpay.get_access_token()
if 'error_code' not in token:
    response = bootpay.publish_automatic_transfer_billing_key(
        receipt_id="66542d4be86c1eedf6b17965",
    )
    # {'receipt_id': '66542d4be86c1eedf6b17965', 'subscription_id': '1716792650.95292', 'gateway_url': 'https://gw.bootpay.co.kr', 'metadata': {}, 'pg': '나이스페이먼츠', 'method': '계좌자동이체', 'method_symbol': 'automatic_transfer_rest', 'method_origin': '계좌자동이체', 'method_origin_symbol': 'automatic_transfer_rest', 'published_at': '2024-05-27T15:53:47+09:00',024-05-27T15:50:51+09:00', 'status_locale': '빌링키발급완료', 'status': 11, 'receipt_data': {'receipt_id': '66542dfb4d18d5fc7b43e1b5', 'order_id': '1716792650.95292', 'price': 1000, 'tax_free': 0, 'cancelled_price': 0, 'cancelled_tax_free': 0, 'order_name': '테스트결제', 'company_name': '윤태섭', 'gateway_url': 'https://gw.bootpay.co.kr', 'metadata': {}, 'sandb: '나이스페이먼츠', 'method': '계좌이체', 'method_symbol': 'bank', 'method_origin': '계좌자동이체', 'method_origin_symbol': 'automatic_transfer_rest', 'purchased_at': '2024-05-27T15:53:47+09:00', 'requested_at': '2024-05-27T15:50:51+09:00', 'status_locale': '결제완료', 'currency': 'KRW', 'receipt_url': 'https://door.bootpay.co.kr/receipt/V2NLSkhkV0UwWGtndXpCRU1veDJJMVNZWWljZElYMVE9LS0zYitsREt0%0Ab0d1amtMMXhNLS15Q0FNRTRSeWgvazRzNXlDQWVlbWZBPT0%3D%0A', 'status': 1, 'bank_data': {'tid': '5155347948', 'bank_code': '004', 'bank_name': '국민', 'bank_account': '0000000000000000', 'bank_username': '윤태*'}}, 'billing_key': '66542dfb4d18d5fc7b43e1b6', 'billing_data': {'bank_name': '국민', 'bank_code': '004', 'bank_account': '0000000000', 'username': '윤태*'}, 'billing_expire_at': '2099-12-31T23:59:59+09:00'}
    print(response)
