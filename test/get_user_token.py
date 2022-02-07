import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from bootpay import Bootpay

bootpay = Bootpay('5b8f6a4d396fa665fdc2b5ea', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')

tokenResponse = bootpay.get_access_token()
if tokenResponse['status'] == 200:
    result = bootpay.get_user_token({
        'user_id': '[[ 회원정보 아이디 ]]', # 필수
        'email': '[[ 회원 이메일 ]]', # 선택
        'name': '[[ 회원 이름 ]]', # 선택
        'gender': '[[ 성별, 0 - 여자, 1 - 남자 ]]', # 선택
        'birth': '[[ 회원 생년 월일 (6자리) ]]', # 선택
        'phone': '[[ 연락가능한 회원 번호 ]]' # 페이앱인 경우 필수, 나머지는 선택
    })
    print(result)
