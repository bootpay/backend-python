"""
Bootpay SDK 테스트 설정

환경에 맞는 키를 선택하여 사용합니다.
"""
import os


def _load_dotenv():
    for file in [os.path.join(os.path.dirname(__file__), '..', '.env'), os.path.join(os.path.dirname(__file__), '.env')]:
        if not os.path.exists(file):
            continue
        with open(file, encoding='utf-8') as fp:
            for raw in fp:
                line = raw.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                os.environ.setdefault(key, value)


def _env(key, fallback):
    return os.environ.get(key, fallback)


_load_dotenv()


# =====================================================
# PG/Commerce API 키 - .env / 환경변수 로 주입한다 (.env.example 참고)
# =====================================================

# PG (ck/sk)
PG_PROD_CLIENT_KEY = _env('BOOTPAY_PG_CLIENT_KEY_PROD', '')
PG_PROD_SECRET_KEY = _env('BOOTPAY_PG_SECRET_KEY_PROD', '')
PG_DEV_CLIENT_KEY = _env('BOOTPAY_PG_CLIENT_KEY_DEV', '')
PG_DEV_SECRET_KEY = _env('BOOTPAY_PG_SECRET_KEY_DEV', '')
# PG legacy application_id/private_key (호환성 검증용)
PG_PROD_APPLICATION_ID = _env('BOOTPAY_PG_APPLICATION_ID_PROD', '5b8f6a4d396fa665fdc2b5ea')
PG_PROD_PRIVATE_KEY = _env('BOOTPAY_PG_PRIVATE_KEY_PROD', 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=')
PG_DEV_APPLICATION_ID = _env('BOOTPAY_PG_APPLICATION_ID_DEV', '59bfc738e13f337dbd6ca48a')
PG_DEV_PRIVATE_KEY = _env('BOOTPAY_PG_PRIVATE_KEY_DEV', 'pDc0NwlkEX3aSaHTp/PPL/i8vn5E/CqRChgyEp/gHD0=')

# Commerce (ck/sk)
COMMERCE_PROD_CLIENT_KEY = _env('BOOTPAY_COMMERCE_CLIENT_KEY_PROD', '')
COMMERCE_PROD_SECRET_KEY = _env('BOOTPAY_COMMERCE_SECRET_KEY_PROD', '')
COMMERCE_DEV_CLIENT_KEY = _env('BOOTPAY_COMMERCE_CLIENT_KEY_DEV', '')
COMMERCE_DEV_SECRET_KEY = _env('BOOTPAY_COMMERCE_SECRET_KEY_DEV', '')

# =====================================================
# 현재 사용할 환경 설정 (development / production)
# =====================================================
CURRENT_ENV = _env('BOOTPAY_ENV', 'production')

# PG 인증 방식: 'new' (client_key/secret_key) 또는 'legacy' (application_id/private_key)
# 매 실행 시 BOOTPAY_AUTH_MODE 환경변수로 토글한다.
AUTH_MODE = (_env('BOOTPAY_AUTH_MODE', 'new') or 'new').lower()

# =====================================================
# 테스트 데이터 (Java SDK 예제와 동일)
# =====================================================
TEST_DATA = {
    # 결제 조회/취소용
    'receipt_id': '628b2206d01c7e00209b6087',
    # 서버 승인용
    'receipt_id_confirm': '62876963d01c7e00209b6028',
    # 현금영수증용
    'receipt_id_cash': '62e0f11f1fc192036b1b3c92',
    # 에스크로용
    'receipt_id_escrow': '628ae7ffd01c7e001e9b6066',
    # 빌링키 조회용 (receipt_id 기반)
    'receipt_id_billing': '62c7ccebcf9f6d001b3adcd4',
    # 계좌 빌링키 발급용
    'receipt_id_transfer': '66541bc4ca4517e69343e24c',
    # 빌링키
    'billing_key': '628b2644d01c7e00209b6092',
    'billing_key_2': '66542dfb4d18d5fc7b43e1b6',
    # 예약 결제 ID
    'reserve_id': '6490149ca575b40024f0b70d',
    'reserve_id_2': '628b316cd01c7e00219b6081',
    # 사용자 ID
    'user_id': '1234',
    # 본인인증 receipt_id
    'certificate_receipt_id': '61b009aaec81b4057e7f6ecd',
}


def _resolve_env(target_env=None):
    return target_env if target_env in ('development', 'production') else CURRENT_ENV


def get_pg_keys(target_env=None):
    """PG API 키 반환 (client_key/secret_key)"""
    env = _resolve_env(target_env)
    if env == 'development':
        return {
            'client_key': PG_DEV_CLIENT_KEY,
            'secret_key': PG_DEV_SECRET_KEY,
            'mode': 'development'
        }
    return {
        'client_key': PG_PROD_CLIENT_KEY,
        'secret_key': PG_PROD_SECRET_KEY,
        'mode': 'production'
    }


def get_pg_legacy_keys(target_env=None):
    """PG legacy 키 반환 (application_id/private_key)"""
    env = _resolve_env(target_env)
    if env == 'development':
        return {
            'application_id': PG_DEV_APPLICATION_ID,
            'private_key': PG_DEV_PRIVATE_KEY,
            'mode': 'development'
        }
    return {
        'application_id': PG_PROD_APPLICATION_ID,
        'private_key': PG_PROD_PRIVATE_KEY,
        'mode': 'production'
    }


def get_active_pg_config(target_env=None):
    """AUTH_MODE 에 따라 BootpayBackend 생성자에 그대로 ** 풀어 넘길 수 있는 dict 반환.

    BOOTPAY_AUTH_MODE=new    → {client_key, secret_key, mode}
    BOOTPAY_AUTH_MODE=legacy → {application_id, private_key, mode}
    """
    env = _resolve_env(target_env)
    if AUTH_MODE == 'legacy':
        print(f"[BOOTPAY_AUTH_MODE=legacy] PG: application_id/private_key (Bearer) | env={env}")
        return get_pg_legacy_keys(env)
    print(f"[BOOTPAY_AUTH_MODE=new] PG: client_key/secret_key (Basic Auth) | env={env}")
    return get_pg_keys(env)


def get_commerce_keys():
    """Commerce API 키 반환"""
    if CURRENT_ENV == 'development':
        return {
            'client_key': COMMERCE_DEV_CLIENT_KEY,
            'secret_key': COMMERCE_DEV_SECRET_KEY,
            'mode': 'development'
        }
    return {
        'client_key': COMMERCE_PROD_CLIENT_KEY,
        'secret_key': COMMERCE_PROD_SECRET_KEY,
        'mode': 'production'
    }
