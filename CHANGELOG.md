### 2.3.0
* 인증: client_key/secret_key Basic Auth 지원 (PG + Commerce 공통).
  * 기존 application_id/private_key Bearer 방식 하위 호환 유지.
  * `BootpayBackend(client_key=..., secret_key=..., mode=...)` 키워드 인자 추가 — application_id/private_key 와 같이 쓸 경우 ck/sk 가 우선.
  * ck/sk 모드는 매 요청 자동 Basic Auth 헤더 부착 — `get_access_token()` 은 합성 응답 (`{access_token: '', expire_in: 0}`) 을 반환하며 `request/token` 호출이 발생하지 않음.
* Commerce: `BootpayCommerce` 의 모든 호출이 ck/sk 로 Basic Auth 사용.
* `get_user_wallets`, `request_wallet_payment` `DeprecationWarning` 처리 — 다음 메이저 버전에서 제거 예정.
* 테스트 인프라: `.env` / `BOOTPAY_AUTH_MODE=new|legacy` / `BOOTPAY_ENV` 토글로 ck/sk · legacy 양쪽 검증. `tests/pg/test_legacy_compatibility.py` 단위 테스트 추가 (HTTP mock 기반).

### 2.2.0
* Commerce API 추가
* 테스트 코드 구조 개선 (config 기반)

### 2.1.2
* 배송등록 api 필드 수정 

### 2.1.1
* 배송등록 api 필드 추가 

### 2.1.0
* 빌링키로 결제 api 추가 

### 2.0.9 
- 빌링키로 빌링키 조회 api 추가 
- 계좌자동이체를 위한 api 추가 

### 2.0.8
- 정기결졔 예약시 metadata 필드 추가

### 2.0.7
- 예약 조회 기능 개발

### 2.0.6
- 본인인증 REST API 요청 기능 추가 

### 2.0.5
- 현금영수증 API 추가

### 2.0.4
- setup.py python_requires, install_requires metadata update 

### 2.0.3
- v2 api update 

### 1.0.5
- 정기결제 예약 api에서 excute_at 오탈자 수정, bankcode import 버그 수정 

### 1.0.4
- 정기결제 예약 api에서 excute_at 파라미터 순서 변경 

### 1.0.3
- 정기결제 예약 api 오타 수정 및 사용자 토큰 발급 데이터 포맷 변경 

### 1.0.2
- subscribe_billing_reserve 함수의 파라미터가 변경되었습니다 

### 1.0.1
- change log 및 주석이 상세하게 추가되었습니다 

### 1.0.0
- subscribe_billing_reserve 함수의 파라미터 순서가 변경되었습니다 