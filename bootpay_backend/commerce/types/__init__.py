# Commerce API Types
from typing import TypedDict, Optional, List, Any, Dict

# Common Types
class ListParams(TypedDict, total=False):
    page: int
    limit: int
    keyword: str


class CommerceAddress(TypedDict, total=False):
    address_id: str
    zipcode: str
    addr1: str
    addr2: str
    phone: str
    name: str
    memo: str
    is_default: bool


class CommerceAddressInstruction(TypedDict, total=False):
    instruction_type: int
    instruction: str


# User Types
class CommerceUserGroupRef(TypedDict, total=False):
    user_group_id: str
    name: str


class CommerceUser(TypedDict, total=False):
    user_id: str
    created_at: str
    updated_at: str

    # 고객 유형
    membership_type: int

    # 고객 정보
    name: str
    phone: str
    email: str
    tel: str
    nickname: str
    bank_username: str
    bank_account: str
    bank_code: str
    comment: str

    # 최종상태
    count: int
    status: int

    # 개인 고객
    gender: int
    birth: str
    individual_extension: Dict[str, Any]

    # 쇼핑몰 회원
    login_id: str
    login_pw: str
    login_type: int

    group_tags: List[str]
    metadata: Dict[str, Any]

    # 인증정보
    auth_sms: bool
    auth_phone: bool
    auth_email: bool
    ci: str
    cd: str

    join_at: str
    join_confirm_type: int
    lasted_at: str

    # 약관 동의
    marketing_accept_type: int
    marketing_accept_create_at: str
    marketing_accept_update_at: str
    term_ids: List[str]

    group: CommerceUserGroupRef

    external_uid: str
    is_external: str
    user_group_id: str


class UserListParams(ListParams, total=False):
    member_type: int
    type: str


class UserTokenResponse(TypedDict, total=False):
    access_token: str
    expired_at: str
    user: CommerceUser


class UserLoginResponse(TypedDict, total=False):
    access_token: str
    expired_at: str
    user: CommerceUser


class MallUserLoginParams(TypedDict, total=False):
    # 회원 로그인 파라미터 (V1 API) — POST /v1/users/login
    login_id: str
    password: str
    # 0: 개인, 1: 사업자 (미지정시 0)
    corporate_type: int
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class MallUserJoinParams(TypedDict, total=False):
    # 회원가입 파라미터 (V1 API) — POST /v1/users/join
    login_id: str
    password: str
    name: str
    email: str
    phone: str
    nickname: str
    gender: int
    birth: str
    # 0: 개인, 1: 사업자 (미지정시 0)
    corporate_type: int
    group: Dict[str, Any]
    idempotency_key: str


# 회원가입 중복 확인 타입 (V1 API) — GET /v1/users/join/{type}
# 'email-exist' | 'id-exist' | 'phone-exist' | 'uid-exist' | 'group-business-number-exist'
MallUserJoinCheckType = str


class MallUserSessionResponse(TypedDict, total=False):
    # 회원 세션 조회 응답 (V1 API)
    user: CommerceUser
    access_token: str
    expired_at: str


# UserGroup Types
class CommerceUserGroup(TypedDict, total=False):
    user_group_id: str
    seller_id: str
    project_id: str
    corporate_type: int

    bank: str
    bank_code: str

    count: int
    last_updated_at: str
    status: int

    phone: str
    email: str
    zipcode: str
    address: str
    address_detail: str
    corporate_extension: Dict[str, Any]
    auth_bank: bool

    company_name: str
    business_number: str
    registration_number: str
    corporate_established: str
    business_type: str
    business_category: str
    ceo_name: str
    auth_company: bool

    manager_name: str
    manager_phone: str
    manager_email: str

    personal_customs_clearance_code: str

    point: int
    accumulation: int
    marketing_accept_type: int
    marketing_accept_create_at: str
    marketing_accept_update_at: str

    use_subscription_aggregate_transaction: bool
    subscription_month_day: int
    subscription_week_day: int

    use_limit: bool
    purchase_limit: int
    subscribed_limit: int
    limit_message: str
    external_uid: str
    is_external: str


# Constants
CORPORATE_TYPE_INDIVIDUAL = 1
CORPORATE_TYPE_CORPORATE = 2


class UserGroupListParams(ListParams, total=False):
    corporate_type: int


class UserGroupLimitParams(TypedDict, total=False):
    user_group_id: str
    use_limit: bool
    limit_month_purchase: int
    limit_week_purchase: int
    purchase_limit: int
    subscribed_limit: int
    limit_message: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class UserGroupAggregateTransactionParams(TypedDict, total=False):
    user_group_id: str
    use_subscription_aggregate_transaction: bool
    subscription_month_day: int
    subscription_week_day: int


# Product Types
class CommerceProductOption(TypedDict, total=False):
    option_id: str
    name: str
    price: int
    stock: int


class CommerceSubscriptionSetting(TypedDict, total=False):
    subscription_setting_id: str
    period_type: str
    period_value: int
    billing_day: int
    billing_count: int


class CommerceProduct(TypedDict, total=False):
    product_id: str
    category_id: str
    project_id: str
    seller_id: str
    subscription_setting_id: str
    delivery_shipping_id: str
    brand_id: str
    manufacturer_id: str

    ex_uid: str

    name: str
    description: str
    images: List[str]
    type: int
    tax_type: int
    use_stock: bool
    stock: int
    use_option_stock: bool
    use_stock_safe: bool
    stock_safe: int

    display_price: int
    tax_free_price: int
    use_discount: bool
    discount_price: int
    discount_price_type: int
    use_discount_period: bool
    discount_start_at: str
    discount_end_at: str

    use_accumulation: bool
    accumulation_point: int
    accumulation_point_type: int

    status_display: bool
    use_display_period: bool
    display_start_at: str
    display_end_at: str
    status_sale: bool
    use_sale_period: bool
    sale_start_at: str
    sale_end_at: str

    count_sale: int
    count_qna: int
    count_like: int
    count_review: int

    barcode: str
    sku: str
    search_tags: List[str]
    event_tags: List[str]
    target_user_tags: List[str]
    delivery_tags: List[str]
    emotion_tags: List[str]

    use_coupon: bool
    use_minor: bool
    use_free_gift: bool
    free_gift: str

    use_bulk_purchase_discount: bool
    bulk_purchase_discount: Dict[str, Any]

    use_review_point: bool
    review_point: Dict[str, Any]

    use_seo: bool
    seo_page_title: str
    seo_meta_description: str
    seo_meta_tags: List[str]

    model_id: str
    model_name: str
    manufacturer_name: str
    brand_name: str
    origin_code: str
    origin_name: str
    importer: str

    used: bool
    expired_at: str
    manufactured_at: str

    use_setup_fee: bool
    setup_fee_value: int
    setup_fee_type: int
    setup_fee_name: str
    setup_fee_text: str

    use_delivery_shipping: bool
    delivery_shipping_fee_type: int
    use_overseas_shipping: bool
    use_delivery_shipping_bundle: bool
    delivery_shipping_bundle_id: str

    use_subscription: bool
    use_subscription_times: bool
    use_product_price: bool

    use_cancel: bool
    use_able_refund: bool
    use_able_cart: bool

    created_at: str
    updated_at: str

    options: List[CommerceProductOption]
    subscription_setting: CommerceSubscriptionSetting


class ProductListParams(ListParams, total=False):
    type: int
    period_type: str
    s_at: str
    e_at: str
    category_code: str


class MallProductListParams(ProductListParams, total=False):
    # 상품 목록 조회 (V1 Mall API) 파라미터
    # ⚠️ keyword 는 서버가 읽지 않는다 (하위호환 때문에 인자는 유지)
    category_id: str
    sort: str
    user_jwt: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, query 에는 포함되지 않는다)
    idempotency_key: str


class ProductStatusParams(TypedDict, total=False):
    # ⚠️ 재고(stock)는 여기가 아니라 update 로 바꾼다.
    product_id: str
    status: int
    status_display: bool
    status_sale: bool
    status_frozen: bool
    status_review: bool
    use_display_period: bool
    display_start_at: str
    display_end_at: str
    use_sale_period: bool
    sale_start_at: str
    sale_end_at: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


# Invoice Types
# Constants
INVOICE_SEND_TYPE_SMS = 1
INVOICE_SEND_TYPE_KAKAO = 2
INVOICE_SEND_TYPE_EMAIL = 3
INVOICE_SEND_TYPE_PUSH = 4


class CommerceInvoiceItem(TypedDict, total=False):
    invoice_item_id: str
    name: str
    price: int
    qty: int
    tax_free_price: int


class CommerceInvoice(TypedDict, total=False):
    invoice_id: str
    project_id: str
    seller_id: str

    name: str
    title: str
    memo: str
    product_name: str

    created_owner_id: str
    created_owner_type: int

    unit: int
    metadata: Dict[str, Any]

    request_id: str
    sku: str

    use_redirect: bool
    redirect_url: str

    type: int
    parent_id: str

    subscription_type: int
    subscription_start_at: str
    subscription_end_at: str

    expired_at: str
    status: int
    deleted: bool

    user_collection_type: int
    use_link_redirect: bool

    user_id: str

    send_status: int
    send_types: List[int]

    message_template_id: str
    message_id: str
    message_from: str
    message_type: int
    message_response: str

    sent_at: str
    pay_at: str

    price: int
    tax_free_price: int

    use_editable_username: bool
    use_editable_phone: bool
    use_editable_email: bool
    use_memo: bool

    product_ids: List[str]
    product_option_ids: List[str]

    tags: List[str]

    password: str
    order_id: str
    uuid: str

    webhook_url: str
    header_content_type: int
    webhook_retry_count: int

    product_type: int
    is_open_link: bool

    invoice_items: List[CommerceInvoiceItem]
    selected_users: List[str]


class InvoiceListParams(ListParams, total=False):
    # limit 미지정시 서버 기본값과 동일한 24 로 전송된다.
    cs_type: str
    user_id: str
    product_type: int
    css_at: str
    cse_at: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, query 에는 포함되지 않는다)
    idempotency_key: str


class InvoiceListResponse(TypedDict, total=False):
    # ⚠️ { items, total } 이 아니라 { list, count } 다.
    list: List[CommerceInvoice]
    count: int


class InvoiceCreateParams(TypedDict, total=False):
    user_id: str
    user_group_id: str
    title: str
    name: str
    description: str
    price: int
    tax_free_price: int
    expired_at: str
    invoice_items: List[CommerceInvoiceItem]
    send_types: List[int]
    webhook_url: str
    metadata: Dict[str, Any]


# Order Types
# Constants
SUBSCRIPTION_BILLING_TYPE_NONE = 0
SUBSCRIPTION_BILLING_TYPE_EACH = 1
SUBSCRIPTION_BILLING_TYPE_GROUP = 2


class CommerceChosenProductOption(TypedDict, total=False):
    chosen_product_option_id: str
    product_id: str
    product_option_id: str
    product_name: str
    option_name: str
    price: int
    tax_free_price: int
    qty: int


class CommerceOrderCancellationRequestHistory(TypedDict, total=False):
    order_cancellation_request_history_id: str
    order_id: str
    status: int
    cancel_reason: str
    cancel_type: int
    requested_at: str
    processed_at: str


class CommerceOrder(TypedDict, total=False):
    order_id: str
    order_pre_id: str
    chosen_product_options: List[CommerceChosenProductOption]

    parent_order_id: str
    user_id: str
    seller_id: str
    project_id: str
    status: int
    currency: int
    is_subscription: bool
    is_leaf: bool
    total_price: int
    tax_free_price: int
    discount_amount: int
    delivery_price: int
    payment_method: str
    receipt_id: str
    webhook_url: str
    created_at: str
    updated_at: str

    cancelled_request_history: List[CommerceOrderCancellationRequestHistory]


class OrderListParams(ListParams, total=False):
    user_id: str
    user_group_id: str
    status: List[int]
    payment_status: List[int]
    cs_type: str
    search_date_from: str
    search_date_to: str
    # css_at / cse_at 는 서버 별칭으로 계속 지원 (정식 키는 search_date_from / search_date_to)
    css_at: str
    cse_at: str
    subscription_billing_type: int
    order_subscription_ids: List[str]


# OrderCancel Types
class OrderCancelListParams(TypedDict, total=False):
    order_id: str
    order_number: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, query 에는 포함되지 않는다)
    idempotency_key: str


class CancelProduct(TypedDict, total=False):
    order_product_id: str
    product_id: str
    qty: int
    cancel_price: int


class CancelOrderSubscriptionBill(TypedDict, total=False):
    order_subscription_bill_id: str
    cancel_price: int


class RequestCancelParameter(TypedDict, total=False):
    cancel_products: List[CancelProduct]
    cancel_order_subscription_bills: List[CancelOrderSubscriptionBill]
    cancel_reason: str
    cancel_type: int
    refund_price: int


class OrderCancelParams(TypedDict, total=False):
    order_number: str
    request_cancel_parameters: RequestCancelParameter
    is_supervisor: bool


class OrderCancelActionParams(TypedDict, total=False):
    # 취소 요청 승인/반려 파라미터 (PUT /v1/order/cancel/{id}/approve · /reject)
    # 정식 이름은 order_cancellation_request_id 이며, 구 이름 order_cancel_request_history_id 도 계속 받는다.
    order_cancellation_request_id: str
    order_cancel_request_history_id: str
    # 서버가 읽는 값은 message 다.
    message: str
    cancel_reason: str
    refund_price: int
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class OrderCancelWithdrawParams(TypedDict, total=False):
    # 취소 요청 철회 파라미터 (PUT /v1/order/cancel/{id}/withdraw)
    order_cancellation_request_id: str
    order_cancel_request_history_id: str
    idempotency_key: str


class CommerceOrderCancelRequestHistory(TypedDict, total=False):
    order_cancel_request_history_id: str
    order_id: str
    order_number: str
    status: int
    cancel_reason: str
    cancel_type: int
    requested_at: str
    processed_at: str
    refund_price: int


# OrderSubscription Types
class CommerceOrderSubscription(TypedDict, total=False):
    order_subscription_id: str
    seller_id: str
    project_id: str
    order_id: str
    order_pre_id: str
    user_id: str
    user_group_id: str
    wallet_id: str

    subscription_billing_type: int
    subscription_payment_cycle_type: int
    subscription_payment_date: int
    subscription_billing_base_day: int

    quantity: int
    is_first_prepaid: bool

    one_unit_price: int
    one_unit_tax_free_price: int
    price: int
    tax_free_price: int
    setup_price: int

    unit: int
    order_name: str
    product_name: str
    option_names: List[str]

    service_start_at: str
    service_end_at: str

    last_billing_created_at: str
    latest_purchased_at: str
    latest_failed_at: str
    payment_next_at: str

    current_duration: int
    created_last_duration: int
    payment_last_duration: int
    total_subscription_duration: int

    membership_type: int
    use_subscription_times: bool

    renewal_status: int
    cancel_status: int
    status: int
    cancel_at: str


class OrderSubscriptionListParams(ListParams, total=False):
    # ⚠️ 날짜 키는 search_date_from / search_date_to (또는 s_at / e_at) 다. orders 의 css_at / cse_at 와 다르다.
    search_date_from: str
    search_date_to: str
    s_at: str
    e_at: str
    request_type: str
    user_group_id: str
    user_id: str
    status: int


class OrderSubscriptionUpdateParams(TypedDict, total=False):
    # 구독 계약 변경 파라미터 — 바뀐 값만 보내면 된다. 서버가 supervisor scope 를 요구한다.
    order_subscription_id: str
    product_id: str
    product_option_id: str
    order_name: str
    total_subscription_duration: int
    quantity: int
    address_id: str
    username: str
    phone: str
    email: str
    use_free_trial: bool
    free_trial_day: int
    service_start_at: str
    next_billing_at: str
    billing_key: str
    status: int
    payment_next_at: str
    service_end_at: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class OrderSubscriptionPauseParams(TypedDict, total=False):
    order_subscription_id: str
    order_number: str
    reason: str
    paused_at: str
    expected_resume_at: str
    idempotency_key: str


class OrderSubscriptionResumeParams(TypedDict, total=False):
    order_subscription_id: str
    order_number: str
    reason: str
    resume_at: str
    idempotency_key: str


class OrderSubscriptionPurchaseParams(TypedDict, total=False):
    # 중도인수 요청 파라미터 (POST /v1/order_subscriptions/requests/ing/purchase)
    order_subscription_id: str
    order_number: str
    price: int
    tax_free_price: int
    reason: str
    idempotency_key: str


class OrderSubscriptionTransferParams(TypedDict, total=False):
    # 구독 이전/승계 요청 파라미터 (POST /v1/order_subscriptions/requests/ing/transfer)
    order_subscription_id: str
    new_user_id: str
    new_username: str
    new_user_email: str
    new_user_phone: str
    new_user_address: str
    wallet_id: str
    reason: str
    idempotency_key: str


class OrderSubscriptionTerminationParams(TypedDict, total=False):
    order_subscription_id: str
    order_number: str
    termination_fee: int
    last_bill_refund_price: int
    final_fee: int
    service_end_at: str
    reason: str
    idempotency_key: str


class CalcTerminateFeeResponse(TypedDict, total=False):
    termination_fee: int
    refund_amount: int
    last_bill_refund_price: int
    final_fee: int


# OrderSubscriptionBill Types
class CommerceOrderSubscriptionBill(TypedDict, total=False):
    order_subscription_bill_id: str
    order_subscription_id: str
    user_id: str
    user_group_id: str

    subscription_billing_type: int
    order_name: str
    paid_wallet_id: str
    reserved_wallet_id: str

    order_number: str
    order_pre_id: str
    order_id: str
    duration: int
    total_subscription_duration: int

    one_unit_price: int
    one_unit_tax_free_price: int
    setup_price: int

    price: int
    tax_free_price: int
    unit: int

    purchase_price: int
    purchase_tax_free_price: int

    cancelled_price: int
    cancelled_tax_free_price: int
    cancelled_fee: int

    membership_type: int

    address_id: str
    user_address: str
    username: str
    user_phone: str
    user_email: str
    user_company_name: str
    user_business_number: str

    product_ids: List[str]
    product_option_ids: List[str]
    product_snapshot_ids: List[str]
    product_option_snapshot_ids: List[str]
    product_type: int
    quantity: int

    reserve_payment_at: str
    purchased_at: str
    revoked_at: str
    last_error_at: str

    status: int
    cancel_status: int
    test_code: str

    service_start_at: str
    service_end_at: str


class OrderSubscriptionBillListParams(ListParams, total=False):
    order_subscription_id: str
    status: List[int]
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, query 에는 포함되지 않는다)
    idempotency_key: str


# OrderSubscriptionAdjustment Types
# Constants
SUBSCRIPTION_ADJUSTMENT_TYPE_PERIOD_DISCOUNT = 1


class CommerceOrderSubscriptionAdjustment(TypedDict, total=False):
    order_subscription_adjustment_id: str
    duration: int
    price: int
    tax_free_price: int
    name: str
    type: int
    created_at: str


class OrderSubscriptionAdjustmentUpdateParams(TypedDict, total=False):
    # 서버는 duration(회차) 단위로 adjustments 배열을 통째로 교체한다. duration 미지정시 1 이 적용된다.
    order_subscription_id: str
    duration: int
    adjustments: List[CommerceOrderSubscriptionAdjustment]
    order_subscription_adjustment_id: str
    price: int
    tax_free_price: int
    name: str
    type: int
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


# Supervisor OrderSubscription Types
class SupervisorOrderSubscriptionApproveParams(TypedDict, total=False):
    reason: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class SupervisorOrderSubscriptionRejectParams(TypedDict, total=False):
    reason: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class SupervisorOrderSubscriptionTerminateParams(TypedDict, total=False):
    reason: str
    termination_fee: int
    last_bill_refund_price: int
    final_fee: int
    service_end_at: str
    cancel_date: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class SupervisorOrderSubscriptionPauseParams(TypedDict, total=False):
    reason: str
    paused_at: str
    expected_resume_at: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class SupervisorOrderSubscriptionResumeParams(TypedDict, total=False):
    reason: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class SupervisorOrderSubscriptionChargeParams(TypedDict, total=False):
    # 수시결제(온디맨드) charge_key 즉시 결제 파라미터
    # charge_key 는 body 로만 전송된다 (URL/query 금지 — 액세스 로그 노출 방지)
    charge_key: str
    price: int
    tax_free_price: int
    user: Dict[str, Any]
    metadata: Dict[str, Any]
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class SupervisorOrderSubscriptionChargeRevokeParams(TypedDict, total=False):
    # 수시결제(온디맨드) charge_key 해지 파라미터
    charge_key: str
    user: Dict[str, Any]
    idempotency_key: str


class OrderSubscriptionChargeResponse(TypedDict, total=False):
    order_id: str
    order_number: str
    receipt_id: str
    charge_key: str
    price: int
    tax_free_price: int
    status: int


class OrderSubscriptionChargeRevokeResponse(TypedDict, total=False):
    charge_key: str
    revoked_at: str
    status: int


# Category Types
class CommerceCategory(TypedDict, total=False):
    category_id: str
    seller_id: str
    project_id: str
    name: str
    parent_category_id: Optional[str]
    parent_categories: List[str]
    status_display: bool
    status_best: bool
    filter_color: int
    filter_size: int
    idx: int
    created_at: str
    updated_at: str


class CategoryCreateParams(TypedDict, total=False):
    name: str
    parent_category_id: str
    status_display: bool
    status_best: bool
    filter_color: int
    filter_size: int
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


class CategoryUpdateParams(TypedDict, total=False):
    category_id: str
    name: str
    parent_category_id: str
    status_display: bool
    status_best: bool
    filter_color: int
    filter_size: int
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str


# Coupon Types
class CommerceCoupon(TypedDict, total=False):
    coupon_id: str
    coupon_template_id: str
    user_id: str
    project_id: str
    name: str
    discount_type: int
    discount_value: int
    min_order_amount: int
    max_discount_amount: int
    status: int
    issued_at: str
    used_at: Optional[str]
    expires_at: Optional[str]
    created_at: str


class CouponListParams(TypedDict, total=False):
    status: str
    page: int
    limit: int


class CouponDownloadParams(TypedDict, total=False):
    coupon_template_id: str


# Point Types
class PointBalance(TypedDict, total=False):
    available_balance: int
    total_earned: int
    total_used: int
    is_negative: bool


class PointTransaction(TypedDict, total=False):
    transaction_id: str
    transaction_type: int
    amount: int
    balance_after: int
    reason: str
    type: int
    order_id: Optional[str]
    review_id: Optional[str]
    earned_at: Optional[str]
    expires_at: Optional[str]
    expired: bool
    remaining_balance: int
    created_at: Optional[str]


class PointTransactionsResponse(TypedDict, total=False):
    transactions: List[PointTransaction]
    total_count: int
    page: int
    limit: int
    total_pages: int


class PointTransactionsParams(TypedDict, total=False):
    page: int
    limit: int
    transaction_type: int


# Cart Types
class CartItemPayload(TypedDict, total=False):
    product_id: str
    product_option_id: str
    quantity: int
    is_subscription: bool
    subscription_period_id: str


class ShippingAddressPayload(TypedDict, total=False):
    zipcode: str


class OrderPreviewParams(TypedDict, total=False):
    member_mode: str
    cart_items: List[CartItemPayload]
    shipping_address: ShippingAddressPayload
    coupon_ids: List[str]
    point_amount: int
    user_group_id: str


class DeliveryGroupItem(TypedDict, total=False):
    cart_item_id: str
    product_id: str
    product_option_id: str
    product_name: str
    quantity: int
    price: int
    subtotal: int


class DeliveryGroup(TypedDict, total=False):
    group_key: str
    seller_id: str
    delivery_shipping_id: str
    delivery_shipping_bundle_id: str
    bundle_id: str
    items: List[DeliveryGroupItem]
    total_price: int
    total_quantity: int
    delivery_fee: int
    delivery_extra_fee_jeju: int
    delivery_extra_fee_remote: int
    shipping_available: bool


class AppliedCouponSnapshot(TypedDict, total=False):
    coupon_id: str
    coupon_template_id: str
    name: str
    discount_type: int
    discount_value: int
    actual_discount_amount: int


class OrderPreviewSummary(TypedDict, total=False):
    total_items: int
    total_quantity: int
    total_product_price: int
    total_delivery_fee: int
    total_delivery_extra_fee: int
    coupon_discount_amount: int
    applied_coupons: List[AppliedCouponSnapshot]
    point_use_amount: int
    point_max_usable: int
    point_balance_after: int
    total_order_price: int


class OrderPreviewUnavailableItem(TypedDict, total=False):
    cart_item_id: str
    product_id: str
    product_name: str
    reason: str


class OrderPreviewResponse(TypedDict, total=False):
    cart_id: str
    user_id: str
    delivery_groups: List[DeliveryGroup]
    summary: OrderPreviewSummary
    unavailable_items: List[OrderPreviewUnavailableItem]


# OrderSubscriptionRequest Types
class OrderSubscriptionRequest(TypedDict, total=False):
    order_subscription_request_history_id: str
    order_subscription_id: str
    project_id: str
    user_id: str
    request_type: int
    status: int
    reason: str
    requested_at: str
    processed_at: Optional[str]
    created_at: str
    updated_at: str


class OrderSubscriptionRequestListParams(TypedDict, total=False):
    project_id: str
    order_subscription_id: str
    page: int
    limit: int
    request_type: int
    status: int
    s_at: str
    e_at: str
    keyword: str
    user_id: str
    user_group_id: str
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, query 에는 포함되지 않는다)
    idempotency_key: str


class OrderSubscriptionRequestUpdateParams(TypedDict, total=False):
    order_subscription_request_history_id: str
    approval: str
    reason: str
    idempotency_key: str


# MallSetting Types
class MallSettingUpdateParams(TypedDict, total=False):
    # 몰 설정 (Mall Setting) — supervisor scope 전용
    # 요청/응답 바디는 flatten 형식이며, 전달된 값(non-None)만 서버로 전송된다.

    # 위젯
    normal_widget_key: str
    subscription_widget_key: str

    # 사업자 정보
    seller_name: str
    seller_name_en: str
    biz_email: str
    biz_tel: str
    biz_fax: str
    registration_no: str
    corp_reg_no: str
    mail_order_sales_number: str
    owner_name: str
    zip: str
    addr_1: str
    addr_2: str
    privacy_name: str
    privacy_email: str

    # 몰 기본 정보
    name: str
    description: str
    status: int
    invoice_title: str

    # 브랜딩
    use_logo: bool
    logo: str
    use_favicon: bool
    favicon: str
    use_open_graph: bool
    og_image: str
    use_signature: bool
    signature: str

    # 고객센터 운영시간
    use_operation_time: bool
    customer_service_center_operation_time: str
    rest_start_hour: int
    rest_start_minute: int
    rest_end_hour: int
    rest_end_minute: int
    # 휴무일 (요일 코드 배열 또는 서버 정의 문자열)
    rest_day: Any
    hosting_service: str

    # 주문/연령 정책
    use_non_member_order: bool
    use_age_accept_19: bool
    use_age_accept_14: bool
    use_age_accept_parent_name: bool
    use_age_accept_parent_birth: bool
    use_age_accept_parent_email: bool

    # 회원가입 수집 항목
    use_membership_collect_phone: bool
    use_membership_collect_tel: bool
    use_membership_collect_email: bool
    use_membership_collect_address: bool
    use_membership_collect_bank: bool
    use_membership_collect_birth: bool
    use_membership_collect_gender: bool
    use_membership_collect_interest: bool
    membership_collect_interest_number: int
    use_membership_collect_customs: bool
    use_membership_collect_nickname: bool
    use_membership_collect_recommend_id: bool
    recommend_id_point_to: int
    recommend_id_point_from: int
    use_membership_collect_business: bool
    use_membership_collect_register: bool
    membership_only_business: bool

    # 기업(그룹) 회원
    use_corporate_department: bool
    sub_group_type: int
    use_corporate_signup_approval: bool
    # 기업 회원 허용 이메일 도메인 목록
    corporate_email_domains: Any
    use_corporate_auto_approve: bool
    use_corporate_invite_only: bool

    # 회원 정보 노출 항목
    use_member_info_phone: bool
    use_member_info_tel: bool
    use_member_info_email: bool
    use_member_info_address: bool
    use_member_info_bank: bool
    use_member_info_birth: bool
    use_member_info_gender: bool
    use_member_info_customs: bool
    use_member_info_nickname: bool
    use_member_info_register: bool

    # 주문자 수집 항목
    orderer_collect_phone: bool
    orderer_collect_tel: bool
    orderer_collect_email: bool

    # 주문/취소 정책
    order_prefix: str
    use_order_cancel: bool
    # 취소 승인 사용 여부 (서버 필드명 오타 그대로 유지)
    use_oder_cancel_approval: bool
    # 취소 사유 목록
    order_cancel_reasons: Any
    order_cancel_reason_required_type: int
    order_cancel_request_message: str
    order_cancel_done_message: str

    # 회원 가입/인증 방식
    use_general_membership: bool
    general_membership_duplication: int
    use_certification: bool
    certification_type: int
    general_membership_id_type: int
    use_membership_duplication_email: bool
    use_membership_duplication_phone: bool
    use_social_membership: bool
    # 사용 소셜 로그인 타입
    social_membership_type: Any

    # 적립금
    use_point: bool
    use_point_transaction: bool
    point_display_name: str
    point_min_balance: int
    # 적립 제외 조건
    point_not_condition: Any
    # 적립 조건
    point_condition: Any
    use_point_max_rate: bool
    point_max_rate: int
    use_point_max_amount: bool
    point_max_amount: int
    point_rate: int
    point_calc_type1: int
    point_calc_type2: int
    use_point_advance_discount: bool
    point_advance_discount_rate: int
    use_point_expire: bool
    point_expire_type: int
    point_issue_event_type: int
    point_issue_delay_days: int

    # 오픈마켓 / 상품
    use_open_market: bool
    use_product_approval: bool
    use_product_review: bool
    use_product_review_point: bool
    product_review_point: int
    product_review_photo_point: int
    use_product_review_answer: bool
    use_product_review_auto_answer: bool
    product_review_auto_answer_minute: int
    product_review_auto_answer_text: str
    use_product_qna: bool
    product_qna_member_auth: int
    use_product_qna_answer_option: bool

    # 게시판 / 상담
    use_notice: bool
    use_qna: bool
    use_faq: bool
    use_chat_support: bool
    chat_support_type: int
    chat_support_key: str

    # 휴면 / 탈퇴
    use_dormant: bool
    dormant_year: int
    dormant_restore: int
    use_withdrawal: bool
    use_withdrawal_guide_message: bool
    use_withdrawal_guide_message_after: bool
    withdrawal_guide_message_after: str
    use_withdrawal_auto: bool
    withdrawal_auto_year: int

    # 정기구독 정산
    use_subscription_aggregate_transaction: bool
    subscription_month_day: int
    subscription_week_day: int

    # 구매 한도
    use_limit: bool
    limit_month_purchase: int
    limit_week_purchase: int
    use_limit_payment: bool
    use_limit_message: bool

    # 약관
    terms_of_service: str
    terms_of_privacy_policy: str
    terms_of_privacy_collect: str
    terms_of_privacy_third: str

    # 결제 / 노출
    payment_timeout: int
    product_sort_type: int
    mall_theme_type: int
    catalog_display_type: int
    catalog_headline: str
    catalog_bg_color: str
    catalog_view_type_pc: int
    catalog_view_type_mobile: int
    catalog_product_sort_type: int

    # 장바구니 / 위시리스트
    use_cart: bool
    cart_storage_period: int
    cart_max_limit: int
    cart_add_action: int
    cart_direct_purchase: bool
    cart_option_change: bool
    cart_discount_display: bool
    use_wishlist: bool
    wishlist_max_limit: int
    cart_wishlist_display: bool


class CommerceMallSetting(MallSettingUpdateParams, total=False):
    mall_setting_id: str
    project_id: str
    seller_id: str
    created_at: str
    updated_at: str


# Webhook Types
class SendTestWebhookParams(TypedDict, total=False):
    # 테스트 웹훅 발송 파라미터 (POST /v1/webhook/test)
    # 웹훅 본문 Content-Type (미지정시 서버 기본값)
    header_content_type: int
    # 미지정시 자동 생성 (Idempotency-Key 헤더로 전송, body 에는 포함되지 않는다)
    idempotency_key: str
