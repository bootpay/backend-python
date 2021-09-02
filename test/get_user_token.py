import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import bootpay

api = bootpay.Api('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

result = bootpay.get_access_token()
print(result)
if result['status'] is 200:
    print(bootpay.get_user_token({
        'user_id': '[[ 회원정보 아이디 ]]', # 필수
        'email': '[[ 회원 이메일 ]]', # 선택
        'name': '[[ 회원 이름 ]]', # 선택
        'gender': '[[ 성별, 0 - 여자, 1 - 남자 ]]', # 선택
        'birth': '[[ 회원 생년 월일 (6자리) ]]', # 선택
        'phone': '[[ 연락가능한 회원 번호 ]]' # 페이앱인 경우 필수, 나머지는 선택
    }))
