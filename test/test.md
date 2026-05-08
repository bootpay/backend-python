# Bootpay Python SDK 테스트 가이드

## 폴더 구조

```
test/
├── config.py           # 공통 설정 (API 키, 환경 설정)
├── pg/                 # PG API 테스트
│   ├── access_token.py
│   ├── authenticate_*.py
│   ├── cancel.py
│   ├── cash_receipt_*.py
│   ├── certificate.py
│   └── ...
└── commerce/           # Commerce API 테스트
    └── test_commerce_basic.py
```

## 환경 설정

`test/config.py`에서 환경을 설정합니다:

```python
# development 또는 production
CURRENT_ENV = 'production'
```

## 테스트 실행 방법

### 1. SDK 설치 확인

프로젝트 루트에서 SDK를 설치합니다:

```bash
cd /Users/taesupyoon/bootpay/server/sdk/python
pip install -e .
```

### 2. PG API 테스트

`test/pg/` 폴더로 이동 후 개별 파일 실행:

```bash
cd test/pg

# 토큰 발급 테스트
python access_token.py

# 결제 조회 테스트
python receipt_payment.py

# 결제 취소 테스트
python cancel.py

# 본인인증 테스트
python certificate.py
python authenticate_request_rest.py
python authenticate_confirm_rest.py
python authenticate_realarm_rest.py

# 빌링키 테스트
python get_billing_key.py
python lookup_billing_key.py
python lookup_subscribe_billing_key.py
python destroy_billing_key.py

# 정기결제 테스트
python request_subscribe_card_payment.py
python request_subscribe_payment.py
python subscribe_payment_reserve.py
python subscribe_payment_reserve_lookup.py
python cancel_subscribe_reserve.py

# 계좌 자동이체 빌링키
python request_subscribe_automatic_transfer_billing_key.py
python publish_automatic_transfer_billing_key.py

# 현금영수증 테스트
python request_cash_receipt.py
python cancel_cash_receipt.py
python cash_receipt_publish_on_receipt.py
python cash_receipt_cancel_on_receipt.py

# 에스크로 테스트
python shipping_start.py

# 사용자 토큰 테스트
python get_user_token.py
```

### 3. Commerce API 테스트

`test/commerce/` 폴더로 이동 후 실행:

```bash
cd test/commerce

# 전체 Commerce 테스트 실행
python test_commerce_basic.py
```

## PG API 테스트 목록

| 파일명 | 설명 |
|--------|------|
| `access_token.py` | 토큰 발급 |
| `receipt_payment.py` | 결제 조회 |
| `cancel.py` | 결제 취소 |
| `certificate.py` | 본인인증 조회 |
| `authenticate_request_rest.py` | 본인인증 요청 |
| `authenticate_confirm_rest.py` | 본인인증 확인 |
| `authenticate_realarm_rest.py` | 본인인증 재알림 |
| `get_billing_key.py` | 빌링키 발급 |
| `lookup_billing_key.py` | 빌링키 조회 |
| `lookup_subscribe_billing_key.py` | 정기결제 빌링키 조회 |
| `destroy_billing_key.py` | 빌링키 삭제 |
| `request_subscribe_card_payment.py` | 카드 정기결제 빌링키 발급 |
| `request_subscribe_payment.py` | 정기결제 실행 |
| `subscribe_payment_reserve.py` | 예약 결제 등록 |
| `subscribe_payment_reserve_lookup.py` | 예약 결제 조회 |
| `cancel_subscribe_reserve.py` | 예약 결제 취소 |
| `request_subscribe_automatic_transfer_billing_key.py` | 계좌 자동이체 빌링키 요청 |
| `publish_automatic_transfer_billing_key.py` | 계좌 자동이체 빌링키 발급 |
| `request_cash_receipt.py` | 현금영수증 발급 |
| `cancel_cash_receipt.py` | 현금영수증 취소 |
| `cash_receipt_publish_on_receipt.py` | 결제건 현금영수증 발급 |
| `cash_receipt_cancel_on_receipt.py` | 결제건 현금영수증 취소 |
| `shipping_start.py` | 에스크로 배송 시작 |
| `get_user_token.py` | 사용자 토큰 발급 |

## Commerce API 테스트 목록

| 파일명 | 설명 |
|--------|------|
| `test_commerce_basic.py` | 토큰, 사용자, 상품, 주문, Role 체이닝 테스트 |

## 주의사항

1. **실제 결제 테스트**: `cancel.py`, `receipt_payment.py` 등은 실제 receipt_id가 필요합니다.
2. **환경 선택**: `config.py`의 `CURRENT_ENV`로 development/production 환경을 선택합니다.
3. **순서 의존성**: 일부 테스트는 다른 테스트 결과(receipt_id, billing_key 등)가 필요합니다.

## PG 인증 방식 토글 (BOOTPAY_AUTH_MODE)

PG 테스트는 기본적으로 신규 `client_key/secret_key` 방식으로 동작한다. 매 실행 시 환경변수로 레거시 `application_id/private_key` 방식으로 전환할 수 있다.

### 토글 contract

| `BOOTPAY_AUTH_MODE` | 동작 |
|---|---|
| `new` (기본, 미설정 시 동일) | `BootpayBackend(client_key=..., secret_key=..., mode=...)` 로 인스턴스 생성. Basic Auth 헤더 자동 부착. |
| `legacy` | `BootpayBackend(application_id=..., private_key=..., mode=...)` 로 인스턴스 생성. `get_access_token()` 호출 후 `Bearer` 헤더 사용. |

키 값은 모두 `.env` (또는 환경변수) 로 주입한다 — `.env.example` 참고.

### 사용법

```bash
# (1) 기본 — env var 생략 (= new)
python test/pg/receipt_payment.py

# (2) 한 번만 legacy 로 전환
BOOTPAY_AUTH_MODE=legacy python test/pg/receipt_payment.py

# (3) pytest 도 동일하게 환경변수로 토글
BOOTPAY_AUTH_MODE=legacy pytest tests/pg

# (4) 셸 세션 동안 legacy 고정
export BOOTPAY_AUTH_MODE=legacy
python test/pg/receipt_payment.py
pytest tests/pg
unset BOOTPAY_AUTH_MODE

# (5) 영구 전환 — .env 의 BOOTPAY_AUTH_MODE 값을 legacy 로 바꾸면 셸 export 없이도 동작
```

### 진입 헬퍼 — 어디서 토글이 흡수되는가

| 테스트 종류 | 위치 | 헬퍼 |
|---|---|---|
| Standalone 스크립트 (`test/pg/*.py`) | `test/config.py` | `get_active_pg_config()` → `BootpayBackend(**cfg)` |
| pytest 통합 테스트 (`tests/pg/*.py`) | `tests/conftest.py` | `pg_client` fixture (PG_KEYS 또는 PG_LEGACY_KEYS 분기) |

PG 테스트 파일들은 다음 한 줄로 두 모드를 모두 지원한다:

```python
# Standalone
bootpay = BootpayBackend(**get_active_pg_config())

# pytest
def test_something(pg_client):
    res = pg_client.receipt_payment(...)
```

### 실행 시 인증 모드 표시

진입 헬퍼가 호출될 때마다 stdout 에 한 줄로 어떤 모드가 활성화됐는지 표시된다 (pytest 는 session-scope fixture 라서 세션당 1회). `pytest -s` 옵션으로 출력 캡처 비활성화 시 즉시 확인:

```
[BOOTPAY_AUTH_MODE=new] PG: client_key/secret_key (Basic Auth) | env=production
[BOOTPAY_AUTH_MODE=legacy] PG: application_id/private_key (Bearer) | env=production
```

### 토글의 영향을 받지 않는 파일

다음 테스트들은 한 함수 안에서 두 모드를 모두 검증하므로 환경변수에 무관하게 동일한 동작을 한다:

- `tests/pg/test_token.py`
- `tests/pg/test_legacy_compatibility.py`
