import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay_backend import BootpayBackend

# bootpay = BootpayBackend('59b731f084382614ebf72215', 'WwDv0UjfwFa04wYG0LJZZv1xwraQnlhnHE375n52X0U=')
bootpay = BootpayBackend('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

token = bootpay.get_access_token() 
if 'error_code' not in token:
    response = bootpay.request_subscribe_billing_key(
        pg='나이스페이',
        order_name='테스트결제',
        subscription_id=str(time.time()),
        card_no="5570********1074", # 카드번호 
        card_pw="**", # 카드 비밀번호 2자리 
        card_identity_no="******", # 카드 소주 생년월일 
        card_expire_year="**", # 카드 유효기간 년 2자리 
        card_expire_month="**",  # 카드 유효기간 월 2자리 

    )
    print(response)
