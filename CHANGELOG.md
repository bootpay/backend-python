### 2.5.0

#### Commerce scope(BOOTPAY-ROLE) 정합성 (동작 변경)

서버(commerce-api)가 `scope_invalid!` 로 supervisor / manager scope 를 요구하는 10개 엔드포인트가 `BOOTPAY-ROLE: user` 로 나가고 있었다. 요청 단위로 올바른 scope 를 붙인다. Java SDK 3.3.0 · Ruby SDK 와 같은 규약이다.

- `order_subscription` — `supervisor_approve` / `supervisor_reject` / `supervisor_terminate` / `supervisor_pause` / `supervisor_resume` → **supervisor**
- `category` — `create` / `update` / `destroy` → **supervisor**
- `user_group` — `user_create` / `user_delete` → **manager**

부수 효과로 이 10개 호출에 `Idempotency-Key` 가 자동 부착된다 (다른 supervisor 메서드·Ruby SDK 와 동일). 요청 경로·바디는 변경 없다.
⚠️ 그동안 이 API 들은 올바른 키로도 scope 오류로 거절됐다. 우회하려고 role 을 직접 조작하던 코드가 있다면 제거해도 된다.

- 파라미터 dict 에 `idempotency_key` (optional) 를 추가했다. 지정하면 그 값이 `Idempotency-Key` 헤더로 나가고 바디에는 실리지 않는다. `category.destroy(category_id, idempotency_key=None)` / `user_group.user_create(user_group_id, user_id, idempotency_key=None)` / `user_group.user_delete(...)` 는 선택 인자로 받는다.
- `tests/commerce/test_wire_format.py` 에 10개 엔드포인트의 scope·Idempotency-Key 회귀 테스트를 추가했다.

### 2.4.0
* NodeJS SDK 2.9.0 parity.
* PG: 우선순위(순차) 결제 빌링키 조회 `lookup_sequential_billing_key(widget_key, billing_key, user_id)` 추가 — `GET subscribe/sequential_billing_key/{billing_key}?widget_key=&user_id=` (쿼리 값 URL 인코딩).
* Commerce: 신규 모듈 추가
  * `mall_setting` — `get_mall_setting`/`detail` (`GET mall-setting`), `update_mall_setting`/`update` (`PUT mall-setting`). supervisor 전용, update 는 flatten 바디에 None 값 미전송.
  * `webhook` — `send_test` (`POST webhook/test`, `header_content_type` 파라미터).
* Commerce: 수시결제(온디맨드) charge_key 결제/해지 추가 (supervisor 전용)
  * `order_subscription.supervisor_charge` (`POST order_subscriptions/charge`) / `supervisor_charge_revoke` (`DELETE order_subscriptions/charge`).
  * charge_key 는 body 로만 전송 (URL/query 금지 — 액세스 로그 노출 방지). `Idempotency-Key` 헤더 자동 생성 (`idempotency_key` 인자로 직접 지정 가능).
* Commerce: 쇼핑몰(V1 Mall API) 회원/상품 endpoint 추가
  * `user.user_login` (`POST users/login`) / `user_session` (`GET users/session`) / `user_logout` (`DELETE users/session`) / `user_join` (`POST users/join`) / `user_join_check` (`GET users/join/{type}?pk=`) / `uid_exist` (`GET users/join/uid-exist?pk=`).
  * 세션이 필요한 호출은 회원 JWT 를 `Bootpay-User-JWT` 헤더로 전달 (값이 있을 때만 부착).
  * `product.products` (`GET products` — page/limit 기본 1/20, category_id/sort/user_jwt 지원) / `product_detail(product_id, user_jwt)`.
* Commerce: `order_subscription.request_ing` 에 `purchase`(중도인수) / `transfer`(이전·승계) 추가.
* Commerce: multipart 전송 정정 — `product.create` 는 이미지 경로 배열이 있으면 multipart/form-data, 없으면 JSON 전송. Rails 는 반복 `images` 를 배열로 받지 않으므로 `images[0]`, `images[1]` … 인덱싱. Content-Type 은 requests 가 생성한 boundary 포함 값을 그대로 사용.
* Commerce: 인자·응답 규약 정정
  * `invoice.list` 응답은 `{ items, total }` 이 아니라 `{ list, count }` — 타입 정정, `limit` 기본값 24, `cs_type`/`user_id`/`product_type`/`css_at`/`cse_at` 파라미터 추가.
  * `invoice.notify` 의 `send_types` 를 선택 인자로 변경 (미전달시 서버가 빈 배열로 처리).
  * `order_cancel.approve`/`reject`/`withdraw` 인자명을 `order_cancellation_request_id` 로 통일 (구 이름 `order_cancel_request_history_id` 도 계속 지원).
  * `order_subscription_adjustment.delete` 는 대상 ID 를 query 가 아니라 body 로 전송. `update` 에 `adjustments` 배열 지원 (서버는 duration 회차 단위 교체).
  * `user_group.limit` 에 `limit_month_purchase`/`limit_week_purchase` 추가 (서버 정식 인자명; `update` 로는 한도가 반영되지 않는다).
  * `order.list` 에 `search_date_from`/`search_date_to` 추가 (`css_at`/`cse_at` 는 서버 별칭으로 계속 지원).
  * `order_subscription.list` 에 `search_date_from`/`search_date_to`/`status` 추가.
  * `order_subscription_request.list` 에 `order_subscription_id`/`user_id`/`user_group_id` 추가.
  * `order_subscription_bill.list` — page/limit 기본값 1/20 상시 전송, `Idempotency-Key` 자동 생성 (`idempotency_key` 인자로 직접 지정 가능), user role.
  * multipart 전송의 bool 값은 소문자 `'true'`/`'false'` 로 직렬화 — 기존 `str()` 방식의 `"False"` 는 Rails 가 true 로 캐스팅하는 위험이 있었다.
* Commerce: 서버가 요구하는 `BOOTPAY-ROLE` scope 를 endpoint 별로 명시 — 상품 쓰기/그룹 한도는 `manager`, 구독 계약변경·조정항목·요청 승인·supervisor_charge·mall_setting 은 `supervisor`, 나머지는 `user`.
  * `order_subscription_request.list`/`detail` 은 `project_id` 가 있으면 `supervisor`, 없으면 `user`.
  * 요청별로 지정된 role 헤더를 공통 계층이 덮어쓰지 않도록 수정.
  * `store.get_store`/`get_store_detail` 에 `Idempotency-Key` 헤더 부착 (인자로 직접 지정 가능).
* 테스트 인프라: 라이브 API 테스트는 `BOOTPAY_ENV=development` 일 때만 실행 (그 외에는 skip) — 무인자 pytest 실행이 production 을 호출하지 않도록 게이트 추가. wire-format(HTTP mock) 테스트 스위트 신설.

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