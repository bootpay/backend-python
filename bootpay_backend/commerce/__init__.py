# Commerce API
from .commerce_resource import BootpayCommerceResource
from .modules import (
    UserModule,
    UserGroupModule,
    ProductModule,
    InvoiceModule,
    OrderModule,
    OrderCancelModule,
    OrderSubscriptionModule,
    OrderSubscriptionBillModule,
    OrderSubscriptionAdjustmentModule
)
from .types import *


class BootpayCommerce(BootpayCommerceResource):
    """
    Bootpay Commerce API 클라이언트

    사용 예시:
    ```python
    from bootpay_backend.commerce import BootpayCommerce

    commerce = BootpayCommerce(
        client_key='your_client_key',
        secret_key='your_secret_key',
        mode='production'  # 'development', 'stage', 'production'
    )

    # 액세스 토큰 발급
    token_response = commerce.get_access_token()

    # 사용자 목록 조회
    users = commerce.user.list({'page': 1, 'limit': 10})

    # Role 설정 (메서드 체이닝 지원)
    commerce.as_manager()
    products = commerce.product.list()
    ```
    """

    def __init__(self, client_key: str = None, secret_key: str = None, mode: str = 'production'):
        """
        BootpayCommerce 초기화

        :param client_key: Commerce API 클라이언트 키
        :param secret_key: Commerce API 시크릿 키
        :param mode: 환경 ('development', 'stage', 'production')
        """
        super().__init__()
        if client_key and secret_key:
            self.set_configuration(client_key, secret_key, mode)
        self._init_modules()

    def _init_modules(self):
        """모듈 초기화"""
        self.user = UserModule(self)
        self.user_group = UserGroupModule(self)
        self.product = ProductModule(self)
        self.invoice = InvoiceModule(self)
        self.order = OrderModule(self)
        self.order_cancel = OrderCancelModule(self)
        self.order_subscription = OrderSubscriptionModule(self)
        self.order_subscription_bill = OrderSubscriptionBillModule(self)
        self.order_subscription_adjustment = OrderSubscriptionAdjustmentModule(self)

    def get_access_token(self):
        """
        액세스 토큰 발급
        client_key/secret_key로 인증

        :return: {'access_token': str, 'expired_at': str}
        """
        response = self.post_with_basic_auth('request/token', {
            'client_key': self.client_key,
            'secret_key': self.secret_key
        })

        if response.get('access_token'):
            self.set_token(response['access_token'])

        return response

    def with_token(self):
        """
        토큰을 발급받아 설정합니다. (메서드 체이닝 지원)

        :return: self
        """
        self.get_access_token()
        return self

    def get_current_token(self) -> str:
        """
        현재 설정된 토큰을 반환합니다.

        :return: 현재 토큰
        """
        return self.get_token()

    def has_token(self) -> bool:
        """
        토큰이 설정되어 있는지 확인합니다.

        :return: 토큰 설정 여부
        """
        token = self.get_token()
        return token is not None and token != ''

    def with_role(self, role: str):
        """
        현재 role을 설정합니다. (메서드 체이닝 지원)

        :param role: 설정할 role
        :return: self
        """
        self.set_role(role)
        return self

    def as_user(self):
        """
        일반 사용자 role로 설정합니다.

        :return: self
        """
        return self.with_role('user')

    def as_manager(self):
        """
        매니저 role로 설정합니다.

        :return: self
        """
        return self.with_role('manager')

    def as_partner(self):
        """
        파트너 role로 설정합니다.

        :return: self
        """
        return self.with_role('partner')

    def as_vendor(self):
        """
        벤더 role로 설정합니다.

        :return: self
        """
        return self.with_role('vendor')

    def as_supervisor(self):
        """
        슈퍼바이저 role로 설정합니다.

        :return: self
        """
        return self.with_role('supervisor')

    def get_current_role(self) -> str:
        """
        현재 role을 반환합니다.

        :return: 현재 role
        """
        return self.get_role()

    def clear_role(self):
        """
        role을 기본값(user)으로 초기화합니다.

        :return: self
        """
        self.set_role('user')
        return self


__all__ = [
    'BootpayCommerce',
    'BootpayCommerceResource',
    'UserModule',
    'UserGroupModule',
    'ProductModule',
    'InvoiceModule',
    'OrderModule',
    'OrderCancelModule',
    'OrderSubscriptionModule',
    'OrderSubscriptionBillModule',
    'OrderSubscriptionAdjustmentModule',
    # Types
    'ListParams',
    'CommerceAddress',
    'CommerceAddressInstruction',
    'CommerceUserGroupRef',
    'CommerceUser',
    'UserListParams',
    'UserTokenResponse',
    'UserLoginResponse',
    'CommerceUserGroup',
    'CORPORATE_TYPE_INDIVIDUAL',
    'CORPORATE_TYPE_CORPORATE',
    'UserGroupListParams',
    'UserGroupLimitParams',
    'UserGroupAggregateTransactionParams',
    'CommerceProductOption',
    'CommerceSubscriptionSetting',
    'CommerceProduct',
    'ProductListParams',
    'ProductStatusParams',
    'INVOICE_SEND_TYPE_SMS',
    'INVOICE_SEND_TYPE_KAKAO',
    'INVOICE_SEND_TYPE_EMAIL',
    'INVOICE_SEND_TYPE_PUSH',
    'CommerceInvoiceItem',
    'CommerceInvoice',
    'InvoiceListParams',
    'InvoiceCreateParams',
    'SUBSCRIPTION_BILLING_TYPE_NONE',
    'SUBSCRIPTION_BILLING_TYPE_EACH',
    'SUBSCRIPTION_BILLING_TYPE_GROUP',
    'CommerceChosenProductOption',
    'CommerceOrderCancellationRequestHistory',
    'CommerceOrder',
    'OrderListParams',
    'OrderCancelListParams',
    'CancelProduct',
    'CancelOrderSubscriptionBill',
    'RequestCancelParameter',
    'OrderCancelParams',
    'OrderCancelActionParams',
    'CommerceOrderCancelRequestHistory',
    'CommerceOrderSubscription',
    'OrderSubscriptionListParams',
    'OrderSubscriptionUpdateParams',
    'OrderSubscriptionPauseParams',
    'OrderSubscriptionResumeParams',
    'OrderSubscriptionTerminationParams',
    'CalcTerminateFeeResponse',
    'CommerceOrderSubscriptionBill',
    'OrderSubscriptionBillListParams',
    'SUBSCRIPTION_ADJUSTMENT_TYPE_PERIOD_DISCOUNT',
    'CommerceOrderSubscriptionAdjustment',
    'OrderSubscriptionAdjustmentUpdateParams',
]
