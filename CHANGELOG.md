### 2.8.1

#### `request_cash_receipt` 의 `pg` 를 선택 파라미터로 (Ruby SDK parity)

별건 현금영수증 발행에서 `pg` 기본값을 `''` 에서 `None` 으로 바꿨다.
빈 문자열은 "PG 를 지정하지 않았다"가 아니라 **이름이 빈 PG 를 지정했다**는 뜻으로 서버에 전달돼,
PG 를 넘기고 싶지 않아도 넘길 수밖에 없었다. 이제 생략하면 `pg: null` 로 나가고
서버가 프로젝트에 설정된 기본 PG 로 발행한다. `pg` 를 명시하던 기존 호출의 동작은 그대로다.

### 2.8.0

#### 알림톡 v1 API 35종 추가 (Ruby SDK parity)

`/v1/alimtalk/*` 를 다루는 모듈 7종을 추가했다. 전부 `BOOTPAY-ROLE: user` 로 나간다 (알림톡 스코프 키가 전부 `user:alimtalk_*`).

* `alimtalk_send` — `send` · `bulk` · `cancel`. ⚠️ **실제로 카카오톡이 발송되고 과금된다. 샌드박스가 없다.**
  멱등은 `ref_id` 로만 성립한다 — 같은 (프로젝트, `ref_id`) 재요청은 기존 receipt 를 돌려주고 실패한 건만 재발송된다.
  ⚠️ `fallback` 은 **미지정(`None`)과 `False` 가 다르다** — `None` 은 프로젝트 기본값, `False` 는 명시적으로 끄는 값이라 `False` 는 그대로 전송한다.
* `alimtalk_message` — `list` · `stats` · `detail`. **유료** 알림톡만 조회된다. 기간 기본값 30일 / 최대 폭 92일이고, 초과분은 거부가 아니라 시작일을 당겨 잘라내므로 실제 구간은 응답의 `period` 로 확인한다.
* `alimtalk_sender` — `categories` · `otp` · `create` · `list` · `detail` · `release` · `variable_examples`. ⚠️ `otp` 는 관리자폰으로 문자를 실제 발송하고 `create` 는 카카오에 발신프로필을 실제 등록한다. 등록 시 그룹키 등록까지 서버가 하므로 공식 템플릿은 별도 채택 없이 바로 발송된다.
* `alimtalk_template` — `list` · `create` · `detail` · `update` · `delete` · `register` · `inspect` · `export` · `image` · `highlight_image`.
  ⚠️ `create` 는 `register: False` 를 주지 않으면 **생성 즉시 대행사·카카오에 실제 등록**된다. `update` 는 부분 수정이 아니라 보내지 않은 필드가 nil 로 덮어써진다.
  `detail` 의 `sync` 는 **서버 기본값이 true** 라 초안 조회에는 `sync=False` 를 권장한다.
* `alimtalk_official` — `list` · `recommend` · `detail`. 부트페이가 미리 승인받아 둔 카탈로그라 검수 없이 즉시 발송된다. 채택 endpoint 는 서버에서 비활성화되어 SDK 에 두지 않는다.
* `alimtalk_optout` — `list` · `create` · `check` · `release`. 발송 판정과 같은 축(전역 + 내 프로젝트)으로 다룬다. ⚠️ 전역 건은 조회는 되지만 해제되지 않고 `global_blocked: True` 로 알려 준다 — "지웠는데 여전히 막히는" 상태를 응답으로 드러내기 위함이다.
* `alimtalk_webhook` — `detail` · `update` · `test` · `rotate_secret` · `deliveries`. ⚠️ **주문·구독 통합 웹훅(`webhook.send_test`)과 완전히 별개 endpoint 다** — 알림톡 이벤트를 기존 주문 웹훅 URL 로 태우면 수신 서버가 모르는 payload 를 받아 기존 연동이 깨진다. 이벤트 코드는 `ALIMTALK_WEBHOOK_EVENT_*` 상수로 노출한다.

#### 알림톡에 Idempotency-Key 를 붙이지 않는다

서버가 알림톡 API 에서는 이 헤더를 읽지 않는다. invoice/product 처럼 무조건 붙이면 서버가 주지 않는 멱등 보장을 주는 것처럼 보여서, 알림톡 모듈만 예외로 뺐다.

#### 전송 계층 보강

* `BootpayCommerceResource.get_raw` 추가 — JSON 이 아닌 본문을 파싱하지 않고 `{'body':, 'content_type':, 'status':}` 로 돌려준다. `alimtalk_template.export(format='csv')` 가 쓴다. 공용 `get` 은 응답을 무조건 `response.json()` 으로 파싱해서, **성공한 요청(200)이 파싱 예외로 실패로 보고**되던 것을 막는다. 그래서 `export` 의 SDK 기본 format 은 서버 기본(csv)이 아니라 **json** 이다.
* `BootpayCommerceResource.post_multipart_file` 추가 — 서버가 필드명을 정해 둔 단일 파일 업로드용(`image`). 기존 `post_multipart` 는 Rails 배열 규약(`images[0]`, `images[1]` ...) 전용이라 그대로 쓰면 서버가 파일을 찾지 못한다. 파일 경로(str)와 열린 파일 객체를 모두 받는다.
* 쿼리스트링의 bool 은 소문자 `true`/`false` 로 직렬화한다 — `urlencode` 의 `'False'` 는 Rails boolean 캐스팅에서 **참**으로 읽혀 `sync=false` 가 `sync=true` 로 뒤집힌다.

### 2.7.0

#### `product.list` 의 조회 필터를 서버 실제 계약에 맞춤

서버(`v1/products_controller#index`)가 읽는 것은 **page · limit · keyword · category_id · ex_uid · sort** 뿐인데,
``product.list()`` 은 정작 그중 `category_id` · `ex_uid` · `sort` 를 **보내지 않고**, 서버가 읽지 않는
`type` · `period_type` · `s_at` · `e_at` · `category_code` 만 보내고 있었다.
필터가 걸린 줄 알았는데 전체 목록이 돌아오는, `member_type` → `membership_type` 과 같은 조용한 실패였다.

- ``ProductListParams`` 에 **`category_id` / `ex_uid` / `sort`** 추가 — 서버가 읽는 값이라 이제 실제로 필터가 걸린다.
- 서버가 읽지 않는 `type` / `period_type` / `s_at` / `e_at` / `category_code` 는 **전송은 그대로 유지**하되(기존 호출 보호) 무시된다는 경고를 문서에 달았다.
  `type` 은 서버의 상품 타입 필터가 문자열(`subscription`/`discount`/`normal`)이라 이 숫자 필드와 값 체계 자체가 다르다.
- ⚠️ `keyword` 는 **26-08-26 서버 변경부터** 실제로 적용된다 (그 이전 배포본에서는 무시된다).
  같은 라운드에서 `GET /v1/products` 의 `sort` 가 항상 무시되던 서버 버그도 함께 고쳤다 — SDK 쪽 변경은 없다.


#### SDK 누락 파라미터 추가 (Ruby SDK parity)

서버는 읽고 있었는데 SDK 에 인자가 없어 쓸 수 없던 파라미터들을 채웠다. 요청 경로·동사·scope 는 모두 변경 없다.

* `order.list` — `order_subscription_ids` / `subscription_billing_type` 로 구독 계약별·결제유형별 필터. `order_subscription_ids` 는 `status` 와 같이 콤마로 join 해서 보낸다 (서버는 콤마 문자열·배열 모두 수용). 값이 비었을 때 `status=` / `payment_status=` 를 실어 보내지 않는다.
* `order_subscription.list` — `order_number` 추가. 주문번호로 구독을 역조회한다.
* `order_subscription.update` — `memo` 추가. 변경이력(SUBSCRIPTION_ACTION_UPDATE)에 남길 사유다.
* `product.products` — `ex_uid` 추가. 외부 UID 로 상품을 찾는다 (`v1/products_controller#index` 가 읽는다).
* `product.lookup_product` — `user_jwt` 추가. `Bootpay-User-JWT` 헤더를 붙여 회원 컨텍스트로 조회한다 — 이제 `product_detail` 과 동작이 같다.
* `user.list` — ⚠️ **회원등급 필터 키 정정.** 서버(`v1/users_controller#index`)가 읽는 이름은 `membership_type` 인데 `member_type` 을 보내고 있어 등급 필터가 **에러 없이 조용히 무시**되고 전체 목록이 돌아왔다. 이제 `membership_type` 으로 보낸다. 기존 호출 호환을 위해 `member_type` 인자는 남기고 `membership_type` 으로 매핑한다 (둘 다 주면 `membership_type` 우선).

### 2.6.0

#### 구독 가격 변경 · 범위로 회차조정 (Ruby SDK parity)

* `order_subscription.update` 에 `price` 추가 — 회차별 결제 금액의 **기준금액**이다. 바꾸면 결제예정(READY) 회차의 청구액이 즉시 다시 계산되고, 이후 회차도 이 금액으로 만들어진다. 이미 결제된 회차는 그대로다. 0 이하는 받지 않는다. 특정 회차만 가감하려면 `order_subscription_adjustment.create` 를 쓴다.
* `order_subscription_adjustment.create` 에 `duration_from` / `duration_to` / `is_unlimited` 추가 — 회차 지정 방법이 3가지가 되었다.
  * `duration: 5` → 5회차 한 건만
  * `duration_from: 3, duration_to: 7` → 3~7회차 각각 한 건씩 (총 5건)
  * `duration_from: 3, is_unlimited: True` → 3회차부터 계약 끝까지 (레코드는 1건, `duration_to` 는 무시)
  * 상한은 계약 총회차이며, 총회차가 무제한인 계약은 60회차까지다. 이미 결제가 끝난 회차는 거절되고, 범위 중 한 회차라도 최종 금액이 음수면 전부 거절된다(부분 반영 없음).
* 요청 경로·동사·scope 는 변경 없다 (`PUT order_subscriptions/{id}` · `POST order_subscriptions/{id}/adjustments`, 둘 다 supervisor).

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