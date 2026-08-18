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


class MallUserJoinParams(TypedDict, total=False):
    login_id: str
    password: str
    name: str
    email: str
    phone: str
    nickname: str
    gender: int
    birth: str
    corporate_type: int
    group: CommerceUserGroupRef


class UserTokenResponse(TypedDict, total=False):
    access_token: str
    expired_at: str
    user: CommerceUser


class UserLoginResponse(TypedDict, total=False):
    access_token: str
    expired_at: str
    user: CommerceUser


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
    purchase_limit: int
    subscribed_limit: int
    limit_month_purchase: int
    limit_week_purchase: int
    limit_message: str


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


class MallProductListParams(ListParams, total=False):
    category_id: str
    sort: str


class ProductStatusParams(TypedDict, total=False):
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
    cs_type: str
    user_id: str
    product_type: int
    css_at: str
    cse_at: str


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
    css_at: str
    cse_at: str
    search_date_from: str
    search_date_to: str
    subscription_billing_type: int
    order_subscription_ids: List[str]


# OrderCancel Types
class OrderCancelListParams(TypedDict, total=False):
    order_id: str
    order_number: str


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
    order_cancellation_request_id: str
    order_cancel_request_history_id: str
    cancel_reason: str
    refund_price: int
    message: str


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
    s_at: str
    e_at: str
    search_date_from: str
    search_date_to: str
    status: int
    request_type: str
    user_group_id: str
    user_id: str


class OrderSubscriptionUpdateParams(TypedDict, total=False):
    order_subscription_id: str
    next_billing_at: str
    billing_key: str
    status: int
    payment_next_at: str
    service_end_at: str
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


class OrderSubscriptionPauseParams(TypedDict, total=False):
    order_subscription_id: str
    order_number: str
    reason: str
    paused_at: str
    expected_resume_at: str


class OrderSubscriptionResumeParams(TypedDict, total=False):
    order_subscription_id: str
    order_number: str
    resume_at: str
    reason: str


class OrderSubscriptionTerminationParams(TypedDict, total=False):
    order_subscription_id: str
    order_number: str
    termination_fee: int
    last_bill_refund_price: int
    final_fee: int
    service_end_at: str
    reason: str


class OrderSubscriptionPurchaseParams(TypedDict, total=False):
    order_subscription_id: str
    price: int
    tax_free_price: int
    reason: str


class OrderSubscriptionTransferParams(TypedDict, total=False):
    order_subscription_id: str
    new_user_id: str
    new_username: str
    new_user_email: str
    new_user_phone: str
    new_user_address: str
    wallet_id: str
    reason: str


class OrderSubscriptionRequestListParams(ListParams, total=False):
    project_id: str
    order_subscription_id: str
    s_at: str
    e_at: str
    status: int
    request_type: str
    user_id: str
    user_group_id: str


class OrderSubscriptionRequestUpdateParams(TypedDict, total=False):
    request_history_id: str
    approval: str
    reason: str
    price: int
    tax_free_price: int
    termination_fee: int
    last_bill_refund_price: int
    final_fee: int
    service_end_at: str


class CalcTerminateFeeResponse(TypedDict, total=False):
    termination_fee: int
    refund_amount: int
    last_bill_refund_price: int
    final_fee: int


class SupervisorOrderSubscriptionApproveParams(TypedDict, total=False):
    reason: str


class SupervisorOrderSubscriptionRejectParams(TypedDict, total=False):
    reason: str


class SupervisorOrderSubscriptionTerminateParams(TypedDict, total=False):
    reason: str
    termination_fee: int
    last_bill_refund_price: int
    final_fee: int
    service_end_at: str
    cancel_date: str


class SupervisorOrderSubscriptionPauseParams(TypedDict, total=False):
    reason: str
    paused_at: str
    expected_resume_at: str


class SupervisorOrderSubscriptionResumeParams(TypedDict, total=False):
    reason: str


class SupervisorOrderSubscriptionChargeParams(TypedDict, total=False):
    charge_key: str
    price: int
    tax_free_price: int
    user: Dict[str, Any]
    metadata: Dict[str, Any]


class SupervisorOrderSubscriptionChargeRevokeParams(TypedDict, total=False):
    charge_key: str
    user: Dict[str, Any]


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
    order_subscription_id: str
    order_subscription_adjustment_id: str
    duration: int
    price: int
    tax_free_price: int
    name: str
    type: int
    adjustments: List[CommerceOrderSubscriptionAdjustment]


# MallSetting Types
class MallSettingUpdateParams(TypedDict, total=False):
    normal_widget_key: str
    subscription_widget_key: str
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
    name: str
    description: str
    status: int
    invoice_title: str
    use_logo: bool
    logo: str
    use_favicon: bool
    favicon: str
    use_open_graph: bool
    og_image: str
    use_signature: bool
    signature: str
    use_operation_time: bool
    customer_service_center_operation_time: Dict[str, Any]
    rest_start_hour: int
    rest_start_minute: int
    rest_end_hour: int
    rest_end_minute: int
    rest_day: List[int]
    hosting_service: str
    use_non_member_order: bool
    use_age_accept_19: bool
    use_age_accept_14: bool
    use_age_accept_parent_name: bool
    use_age_accept_parent_birth: bool
    use_age_accept_parent_email: bool
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
    use_corporate_department: bool
    sub_group_type: int
    use_corporate_signup_approval: bool
    corporate_email_domains: List[str]
    use_corporate_auto_approve: bool
    use_corporate_invite_only: bool
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
    orderer_collect_phone: bool
    orderer_collect_tel: bool
    orderer_collect_email: bool
    order_prefix: str
    use_order_cancel: bool
    use_oder_cancel_approval: bool
    order_cancel_reasons: List[str]
    order_cancel_reason_required_type: int
    order_cancel_request_message: str
    order_cancel_done_message: str
    use_general_membership: bool
    general_membership_duplication: int
    use_certification: bool
    certification_type: int
    general_membership_id_type: int
    use_membership_duplication_email: bool
    use_membership_duplication_phone: bool
    use_social_membership: bool
    social_membership_type: List[int]
    use_point: bool
    use_point_transaction: bool
    point_display_name: str
    point_min_balance: int
    point_not_condition: Any
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
    use_notice: bool
    use_qna: bool
    use_faq: bool
    use_chat_support: bool
    chat_support_type: int
    chat_support_key: str
    use_dormant: bool
    dormant_year: int
    dormant_restore: bool
    use_withdrawal: bool
    use_withdrawal_guide_message: bool
    use_withdrawal_guide_message_after: bool
    withdrawal_guide_message_after: str
    use_withdrawal_auto: bool
    withdrawal_auto_year: int
    use_subscription_aggregate_transaction: bool
    subscription_month_day: int
    subscription_week_day: int
    use_limit: bool
    limit_month_purchase: int
    limit_week_purchase: int
    use_limit_payment: bool
    use_limit_message: bool
    terms_of_service: str
    terms_of_privacy_policy: str
    terms_of_privacy_collect: str
    terms_of_privacy_third: str
    payment_timeout: int
    product_sort_type: int
    mall_theme_type: int
    catalog_display_type: int
    catalog_headline: str
    catalog_bg_color: str
    catalog_view_type_pc: int
    catalog_view_type_mobile: int
    catalog_product_sort_type: int
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
