import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay import Bootpay

bootpay = Bootpay('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

# result = bootpay.get_access_token()
# if result['status'] is 200:
print(bootpay.remote_form(
    {
        'pg': 'danal',
        'fm': ['card', 'phone'],
        'n': '테스트 결제', # 상품명
        'o_key': 'unique_value_1234',  # 가맹점의 상품 고유 키
        'is_r_n': False, # 구매자가 상품명 입력 허용할지 말지
        'is_r_p': False, # 구매자가 가격 입력 허용할지 말지
        'is_addr': False, # 주소창 추가 할지 말지
        'is_da': False, # 배송비 추가 할지 말지
        'is_memo': False,  # 구매자로부터 메모를 받을 지
        'tfp': 0, # 비과세 금액
        'ip': 10000, # 아이템 판매금액
        'dp': 0, # 디스플레이용 가격, 할인전 가격을 의미함, 쿠폰이나 프로모션에 의한 가격 디스카운트 개념 필요 - 페이코 때문에 생긴 개념
        'dap': 0,  # 기본배송비
        'dap_jj': 0, # 제주 배송비
        'dap_njj': 0 # 제주 외 지역 도서산간 추가비용
    },
    {
        # st: 1, #1: sms, 2:lms, 3:mms, 4:알림톡, 5:친구톡
        # rps: ['010-1234-5678', '010-1111-2222'], # 받는 사람 전화번호
        # sp: '010-1234-1111', # 보내는 사람 전화번호
        # msg: '테스트 문자입니다'
    }
))
