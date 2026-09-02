"""
Commerce API - Alimtalk Template Create (알림톡 자체 템플릿 생성) 테스트

⚠️ register 를 False 로 주지 않으면 생성 즉시 대행사·카카오에 실제 등록된다.
"""

import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')

from bootpay_backend.commerce import BootpayCommerce
from config import get_commerce_keys

# 환경에 맞는 키 가져오기
keys = get_commerce_keys()
CLIENT_KEY = keys['client_key']
SECRET_KEY = keys['secret_key']
MODE = keys['mode']


def main():
    """알림톡 자체 템플릿 생성 테스트"""
    commerce = BootpayCommerce(
        client_key=CLIENT_KEY,
        secret_key=SECRET_KEY,
        mode=MODE
    )

    try:
        commerce.get_access_token()

        # 초안만 만들고(register=False) 내용을 확인한 뒤 register 로 올리는 것을 권장한다.
        # 본문 변수는 #{변수명} 형식이고 템플릿 전체에서 최대 40개다.
        response = commerce.alimtalk_template.create({
            'ksp_id': 'KSP_ID_HERE',
            'name': '주문완료 안내',
            'content': '#{user_name}님, #{company_name} 주문이 완료되었습니다.',
            'msg_type': 'BA',
            'emphasize_type': 'NONE',
            'register': False,
            'examples': {
                'user_name': '홍길동',
                'company_name': '부트페이몰'
            }
        })
        print('=== Alimtalk Template Create Response ===')
        print(response)

        template_id = response.get('template_id') or 'TEMPLATE_ID_HERE'

        # 초안 조회는 sync=False 를 권장한다 (서버 기본값이 True 라 벤더 동기화가 일어난다).
        print('\n=== Alimtalk Template Detail Response ===')
        print(commerce.alimtalk_template.detail(template_id, sync=False))

        # 수정은 부분 수정이 아니다 — 보내지 않은 필드는 nil 로 덮어써진다.
        print('\n=== Alimtalk Template Update Response ===')
        print(commerce.alimtalk_template.update(template_id, {
            'name': '주문완료 안내(수정)',
            'content': '#{user_name}님, #{company_name} 주문이 완료되었습니다.',
            'msg_type': 'BA',
            'emphasize_type': 'NONE'
        }))

        # 초안 → 대행사 등록 → 검수 요청 (검수는 카카오에 요청되며 취소할 수 없다)
        print('\n=== Alimtalk Template Register Response ===')
        print(commerce.alimtalk_template.register(template_id))
        print('\n=== Alimtalk Template Inspect Response ===')
        print(commerce.alimtalk_template.inspect(template_id))

        # 목록에는 페이지네이션이 없다 — 필터에 걸린 템플릿을 한 번에 모두 돌려준다.
        print('\n=== Alimtalk Template List Response ===')
        print(commerce.alimtalk_template.list({'ins': 3, 'sort': 'latest'}))

        # 내보내기 기본 format 은 json 이다 (서버 기본은 csv).
        # csv 를 주면 파싱 없이 {'body':, 'content_type':, 'status':} 로 원문을 돌려준다.
        print('\n=== Alimtalk Template Export Response ===')
        print(commerce.alimtalk_template.export({'scope': 'private'}))

        # 이미지형 본문 이미지: jpg/png · 500KB 이하 · 가로 500px 이상 · 2:1
        # 아이템리스트형 하이라이트 썸네일: 가로 108px 이상 · 1:1 (규격이 다르므로 endpoint 가 별도다)
        # print(commerce.alimtalk_template.image('/path/to/banner.jpg'))
        # print(commerce.alimtalk_template.highlight_image('/path/to/thumb.jpg'))
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()
