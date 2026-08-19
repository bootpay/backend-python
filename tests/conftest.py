import os


def _load_dotenv():
    for file in [os.path.join(os.path.dirname(__file__), "..", ".env"), os.path.join(os.path.dirname(__file__), ".env")]:
        if not os.path.exists(file):
            continue
        with open(file, encoding="utf-8") as fp:
            for raw in fp:
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip("\"").strip("'"))


def _env(key, fallback):
    return os.environ.get(key, fallback)


_load_dotenv()
import pytest
from bootpay_backend.rest_client import BootpayBackend
from bootpay_backend.commerce import BootpayCommerce


# ---------------------------------------------------------------------------
# Key configuration by environment
# ---------------------------------------------------------------------------
# 키는 .env / 환경변수 로 주입한다 (.env.example 참고)
PG_KEYS = {
    'development': {
        'client_key': _env('BOOTPAY_PG_CLIENT_KEY_DEV', ''),
        'secret_key': _env('BOOTPAY_PG_SECRET_KEY_DEV', ''),
    },
    'production': {
        'client_key': _env('BOOTPAY_PG_CLIENT_KEY_PROD', ''),
        'secret_key': _env('BOOTPAY_PG_SECRET_KEY_PROD', ''),
    },
}

# Legacy application_id/private_key (호환성 검증용). ck/sk 와 별개로 유지하여 두 인증 모드를 모두 테스트한다.
PG_LEGACY_KEYS = {
    'development': {
        'application_id': _env('BOOTPAY_PG_APPLICATION_ID_DEV', ''),
        'private_key': _env('BOOTPAY_PG_PRIVATE_KEY_DEV', ''),
    },
    'production': {
        'application_id': _env('BOOTPAY_PG_APPLICATION_ID_PROD', ''),
        'private_key': _env('BOOTPAY_PG_PRIVATE_KEY_PROD', ''),
    },
}

COMMERCE_KEYS = {
    'development': {
        'client_key': _env('BOOTPAY_COMMERCE_CLIENT_KEY_DEV', ''),
        'secret_key': _env('BOOTPAY_COMMERCE_SECRET_KEY_DEV', ''),
    },
    'production': {
        'client_key': _env('BOOTPAY_COMMERCE_CLIENT_KEY_PROD', ''),
        'secret_key': _env('BOOTPAY_COMMERCE_SECRET_KEY_PROD', ''),
    },
}

# 테스트 데이터 (nodejs/test/config.js TEST_DATA 와 1:1 mirror).
TEST_DATA = {
    'receipt_id': '628b2206d01c7e00209b6087',
    'receipt_id_confirm': '62876963d01c7e00209b6028',
    'receipt_id_cash': '62e0f11f1fc192036b1b3c92',
    'receipt_id_escrow': '628ae7ffd01c7e001e9b6066',
    'receipt_id_billing': '62c7ccebcf9f6d001b3adcd4',
    'receipt_id_transfer': '66541bc4ca4517e69343e24c',
    'billing_key': '628b2644d01c7e00209b6092',
    'billing_key_2': '66542dfb4d18d5fc7b43e1b6',
    'reserve_id': '6490149ca575b40024f0b70d',
    'reserve_id_2': '628b316cd01c7e00219b6081',
    'user_id': '1234',
    'certificate_receipt_id': '69fd7187564d1f550535538c',
}


def _get_env() -> str:
    """Return the target environment (default: production)."""
    return os.environ.get('BOOTPAY_ENV', 'production')


def _get_auth_mode() -> str:
    """PG 인증 방식: 'new' (client_key/secret_key) 또는 'legacy' (application_id/private_key)."""
    return os.environ.get('BOOTPAY_AUTH_MODE', 'new').lower()


def _require_development(env: str):
    """
    라이브 API 테스트 게이트 — production 실호출 방지.
    무인자 pytest 실행(.env 기본 production)에서는 라이브 테스트 전체를 skip 하고,
    BOOTPAY_ENV=development 로 명시했을 때만 실제 API 를 호출한다.
    (mock 기반 테스트는 이 fixture 를 쓰지 않으므로 영향 없음)
    """
    if env != 'development':
        pytest.skip(f'live API tests run only with BOOTPAY_ENV=development (current: {env})')


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope='session')
def bootpay_env():
    """Current Bootpay environment name."""
    return _get_env()


@pytest.fixture(scope='session')
def pg_client(bootpay_env):
    """
    PG API client. BOOTPAY_AUTH_MODE 에 따라 ck/sk(default) 또는 legacy application_id/private_key 로 인증.
    Shared across the entire test session.
    """
    _require_development(bootpay_env)
    if _get_auth_mode() == 'legacy':
        print(f"[BOOTPAY_AUTH_MODE=legacy] PG: application_id/private_key (Bearer) | env={bootpay_env}")
        legacy = PG_LEGACY_KEYS[bootpay_env]
        client = BootpayBackend(
            application_id=legacy['application_id'],
            private_key=legacy['private_key'],
            mode=bootpay_env,
        )
        # legacy 방식은 토큰 발급 필요.
        token_res = client.get_access_token()
        assert 'error_code' not in token_res, f"PG legacy token failed: {token_res}"
        return client

    print(f"[BOOTPAY_AUTH_MODE=new] PG: client_key/secret_key (Basic Auth) | env={bootpay_env}")
    keys = PG_KEYS[bootpay_env]
    client = BootpayBackend(
        client_key=keys['client_key'],
        secret_key=keys['secret_key'],
        mode=bootpay_env,
    )
    # ck/sk 는 매 요청 Basic Auth 헤더로 직접 인증되므로 토큰 발급 불필요.
    return client


@pytest.fixture(scope='session')
def commerce_client(bootpay_env):
    """
    Commerce API client with a valid access token.
    Shared across the entire test session.
    """
    _require_development(bootpay_env)
    keys = COMMERCE_KEYS[bootpay_env]
    client = BootpayCommerce(
        client_key=keys['client_key'],
        secret_key=keys['secret_key'],
        mode=bootpay_env,
    )
    token_res = client.get_access_token()
    assert token_res.get('access_token'), f"Commerce token failed: {token_res}"
    return client
