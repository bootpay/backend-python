import os
import pytest
from bootpay_backend.rest_client import BootpayBackend
from bootpay_backend.commerce import BootpayCommerce


# ---------------------------------------------------------------------------
# Key configuration by environment
# ---------------------------------------------------------------------------
PG_KEYS = {
    'development': {
        'application_id': '59bfc738e13f337dbd6ca48a',
        'private_key': 'pDc0NwlkEX3aSaHTp/PPL/i8vn5E/CqRChgyEp/gHD0=',
    },
    'production': {
        'application_id': '5b8f6a4d396fa665fdc2b5ea',
        'private_key': 'rm6EYECr6aroQVG2ntW0A6LpWnkTgP4uQ3H18sDDUYw=',
    },
}

COMMERCE_KEYS = {
    'development': {
        'client_key': 'hxS-Up--5RvT6oU6QJE0JA',
        'secret_key': 'r5zxvDcQJiAP2PBQ0aJjSHQtblNmYFt6uFoEMhti_mg=',
    },
    'production': {
        'client_key': 'sEN72kYZBiyMNytA8nUGxQ',
        'secret_key': 'rnZLJamENRgfwTccwmI_Uu9cxsPpAV9X2W-Htg73yfU=',
    },
}


def _get_env() -> str:
    """Return the target environment (default: development)."""
    return os.environ.get('BOOTPAY_ENV', 'development')


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
    PG API client with a valid access token.
    Shared across the entire test session.
    """
    keys = PG_KEYS[bootpay_env]
    client = BootpayBackend(
        application_id=keys['application_id'],
        private_key=keys['private_key'],
        mode=bootpay_env,
    )
    token_res = client.get_access_token()
    assert 'error_code' not in token_res, f"PG token failed: {token_res}"
    return client


@pytest.fixture(scope='session')
def commerce_client(bootpay_env):
    """
    Commerce API client with a valid access token.
    Shared across the entire test session.
    """
    keys = COMMERCE_KEYS[bootpay_env]
    client = BootpayCommerce(
        client_key=keys['client_key'],
        secret_key=keys['secret_key'],
        mode=bootpay_env,
    )
    token_res = client.get_access_token()
    assert token_res.get('access_token'), f"Commerce token failed: {token_res}"
    return client
