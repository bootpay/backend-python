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
CURRENT_ENV = 'development'
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
