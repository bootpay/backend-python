import base64
import requests
import urllib.parse
import warnings


class BootpayBackend:
    BASE_URL = {
        'development': 'https://dev-api.bootpay.co.kr/v2',
        'stage': 'https://stage-api.bootpay.co.kr/v2',
        'production': 'https://api.bootpay.co.kr/v2'
    }
    API_VERSION = '5.1.0'
    SDK_VERSION = '2.7.0'

    def __init__(self, application_id=None, private_key=None, mode='production', client_key=None, secret_key=None):
        # application_id/private_key는 legacy 사용자를 위해 그대로 지원한다.
        # client_key/secret_key가 있으면 새 Basic Auth 방식이 우선된다.
        self.application_id = application_id
        self.private_key = private_key
        self.client_key = client_key
        self.secret_key = secret_key
        self.mode = mode
        self.token = None
        self.api_version = self.API_VERSION

    # API entrypoints
    # Comment by GOSOMI
    # @param url:string
    # @returns string
    def __entrypoints(self, url):
        return '/'.join([self.BASE_URL[self.mode], url])

    def set_api_version(self, version):
        self.api_version = version

    def __authorization(self):
        if self.client_key and self.secret_key:
            credentials = f'{self.client_key}:{self.secret_key}'.encode('utf-8')
            return 'Basic ' + base64.b64encode(credentials).decode('utf-8')
        if self.token is not None:
            return f"Bearer {self.token}"
        return None

    def __validate_credential_pairs(self):
        """지원하는 두 인증 쌍이 각각 완전한지 네트워크 요청 전에 검사한다."""
        has_client_key = bool(self.client_key)
        has_secret_key = bool(self.secret_key)
        has_application_id = bool(self.application_id)
        has_private_key = bool(self.private_key)

        if has_client_key != has_secret_key:
            missing = 'secret_key' if has_client_key else 'client_key'
            raise ValueError(f'{missing} 값이 비어있습니다. client_key와 secret_key는 함께 지정해야 합니다.')
        if has_application_id != has_private_key:
            missing = 'private_key' if has_application_id else 'application_id'
            raise ValueError(
                f'{missing} 값이 비어있습니다. application_id와 private_key는 함께 지정해야 합니다.'
            )

    def __require_authentication(self):
        """일반 PG 요청에 사용할 수 있는 인증 방식이 준비됐는지 검사한다."""
        self.__validate_credential_pairs()
        if self.client_key and self.secret_key:
            return
        if self.application_id and self.private_key and self.token:
            return
        if self.application_id and self.private_key:
            raise RuntimeError(
                'legacy application_id/private_key 인증은 get_access_token()으로 토큰을 먼저 발급해야 합니다.'
            )
        raise ValueError(
            '인증 정보가 없습니다. client_key/secret_key 또는 application_id/private_key를 지정하세요.'
        )

    # Request Rest
    # Comment by GOSOMI
    # @param method: string, url: string, data: object, headers: object
    # @returns ResponseForamt
    def __request(self, method='', url='', data=None, headers=None, params=None):
        self.__require_authentication()
        headers = headers or {}
        params = params or {}
        default_headers = {
            'Accept': 'application/json',
            'BOOTPAY-API-VERSION': self.api_version,
            'BOOTPAY-SDK-VERSION': self.SDK_VERSION,
            'BOOTPAY-SDK-TYPE': '302'
        }
        authorization = self.__authorization()
        if authorization:
            default_headers['Authorization'] = authorization

        if method in ['put', 'post']:
            response = getattr(requests, method)(url, json=data, headers=dict(headers, **default_headers), params=params)
        else:
            response = getattr(requests, method)(url, headers=dict(headers, **default_headers), params=params)
        return response.json()

    # Get AccessToken
    # Comment by GOSOMI
    def get_access_token(self):
        self.__validate_credential_pairs()
        # client_key/secret_key 인증은 매 요청에 Basic Auth 헤더가 자동 부착된다.
        # request/token 호출이 불필요하므로 합성 응답을 즉시 반환한다.
        if self.client_key and self.secret_key:
            self.token = ''
            return {'access_token': '', 'expire_in': 0}
        if not self.application_id and not self.private_key:
            raise ValueError(
                '인증 정보가 없습니다. client_key/secret_key 또는 application_id/private_key를 지정하세요.'
            )
        data = {
            'application_id': self.application_id,
            'private_key': self.private_key
        }
        # 토큰 발급 요청 자체에는 아직 Bearer 토큰이 없으므로 일반 요청 검사를 거치지 않는다.
        headers = {
            'Accept': 'application/json',
            'BOOTPAY-API-VERSION': self.api_version,
            'BOOTPAY-SDK-VERSION': self.SDK_VERSION,
            'BOOTPAY-SDK-TYPE': '302'
        }
        response = requests.post(
            self.__entrypoints('request/token'),
            json=data,
            headers=headers,
            params={}
        ).json()
        if 'error_code' not in response:
            self.token = response['access_token']
        return response

    # Get Receipt Payment Data
    # Comment by GOSOMI
    # @param receipt_id: string
    def receipt_payment(self, receipt_id='', lookup_user_data=False):
        return self.__request(method='get', url=self.__entrypoints(
            f'receipt/{receipt_id}?lookup_user_data={lookup_user_data and "true" or "false"}'))

    # certificate
    # Comment by GOSOMI
    # @param receipt_id: string
    def certificate(self, receipt_id=''):
        return self.__request(method='get', url=self.__entrypoints(f'certificate/{receipt_id}'))

    # confirm payment
    # Comment by GOSOMI
    # @param receipt_id: string
    def confirm_payment(self, receipt_id=''):
        return self.__request(method='post', url=self.__entrypoints('confirm'), data={"receipt_id": receipt_id})

    # lookup subscribe billing key
    # Comment by GOSOMI
    # @param receipt_id:string
    def lookup_subscribe_billing_key(self, receipt_id=''):
        return self.__request(method='get', url=self.__entrypoints(f'subscribe/billing_key/{receipt_id}'))


    # lookup billing key by billing_key
    # Comment by ehowlsla
    # @param billing_key:string
    def lookup_billing_key(self,  billing_key=''):
        return self.__request(method='get', url=self.__entrypoints(f'billing_key/{billing_key}'))


    # lookup sequential billing key
    # 우선순위(순차) 결제 빌링키 조회
    # @param widget_key: string
    # @param billing_key: string
    # @param user_id: string 조회 대상 회원 ID (서버가 빌링키 소유자 검증에 사용한다)
    def lookup_sequential_billing_key(self, widget_key='', billing_key='', user_id=''):
        encoded_widget_key = urllib.parse.quote(widget_key, safe='')
        encoded_user_id = urllib.parse.quote(user_id, safe='')
        return self.__request(method='get', url=self.__entrypoints(
            f'subscribe/sequential_billing_key/{billing_key}?widget_key={encoded_widget_key}&user_id={encoded_user_id}'))


    # request subscribe billing key
    # Comment by GOSOMI
    def request_subscribe_billing_key(self, pg='', order_name='', subscription_id='', card_no='', card_pw='',
                                      card_identity_no='', card_expire_year='', card_expire_month='', method=None, price=0,
                                      tax_free=0, extra=None, user=None, metadata=None):
        return self.__request(method='post', url=self.__entrypoints('request/subscribe'), data={
            "pg": pg,
            "order_name": order_name,
            "subscription_id": subscription_id,
            "card_no": card_no,
            "card_pw": card_pw,
            "card_identity_no": card_identity_no,
            "card_expire_year": card_expire_year,
            "card_expire_month": card_expire_month,
            "method": method,
            "price": price,
            "tax_free": tax_free,
            "extra": extra,
            "user": user,
            "metadata": metadata
        })

    # request subscribe card payment
    # Comment by GOSOMI
    def request_subscribe_card_payment(self, billing_key='', order_name='', price=0, tax_free=0, card_quota='00',
                                       card_interest=None, order_id='', items=None, user=None, extra=None,
                                       feedback_url=None, content_type=None, metadata=None):
        return self.__request(method='post', url=self.__entrypoints('subscribe/payment'), data={
            "billing_key": billing_key,
            "order_name": order_name,
            "price": price,
            "tax_free": tax_free,
            "card_quota": card_quota,
            "card_interest": card_interest,
            "order_id": order_id,
            "items": items,
            "user": user,
            "extra": extra,
            "feedback_url": feedback_url,
            "content_type": content_type,
            "metadata": metadata
        })

    # request subscribe payment
    # Comment by ehowlsla
    def request_subscribe_payment(self, billing_key='', order_name='', price=0, tax_free=0, card_quota='00',
                                       card_interest=None, order_id='', items=None, user=None, extra=None,
                                       feedback_url=None, content_type=None, metadata=None):
        return self.__request(method='post', url=self.__entrypoints('subscribe/payment'), data={
            "billing_key": billing_key,
            "order_name": order_name,
            "price": price,
            "tax_free": tax_free,
            "card_quota": card_quota,
            "card_interest": card_interest,
            "order_id": order_id,
            "items": items,
            "user": user,
            "extra": extra,
            "feedback_url": feedback_url,
            "content_type": content_type,
            "metadata": metadata
        })

    # destroy billing key
    # Comment by GOSOMI
    def destroy_billing_key(self, billing_key=''):
        return self.__request(method='delete', url=self.__entrypoints(f'subscribe/billing_key/{billing_key}'))

    # request user token
    # Comment by GOSOMI
    def request_user_token(self, user_id='', email=None, username=None, gender=None, birth=None, phone=None):
        return self.__request(method='post', url=self.__entrypoints('request/user/token'), data={
            "user_id": user_id,
            "email": email,
            "username": username,
            "gender": gender,
            "birth": birth,
            "phone": phone
        })

    # subscribe payment reserve
    # Comment by GOSOMI
    def subscribe_payment_reserve(self, billing_key='', order_name='', price=0, tax_free=0, order_id='', items=None, metadata={},
                                  user=None, reserve_execute_at='', feedback_url='', content_type=''):
        return self.__request(method='post', url=self.__entrypoints('subscribe/payment/reserve'), data={
            "billing_key": billing_key,
            "order_name": order_name,
            "price": price,
            "metadata": metadata,
            "tax_free": tax_free,
            "order_id": order_id,
            "items": items,
            "user": user,
            "reserve_execute_at": reserve_execute_at,
            "feedback_url": feedback_url,
            "content_type": content_type
        })

    def cancel_payment(self, receipt_id='', cancel_id='', cancel_username='', cancel_message='', cancel_price=None,
                       metadata={}, cancel_tax_free=None, refund=None, items=None):
        return self.__request(method='post', url=self.__entrypoints('cancel'), data={
            "receipt_id": receipt_id,
            "cancel_id": cancel_id,
            "metadata": metadata,
            "cancel_username": cancel_username,
            "cancel_message": cancel_message,
            "cancel_price": cancel_price,
            "cancel_tax_free": cancel_tax_free,
            "refund": refund,
            "items": items
        })

    # subscribe payment reserve lookup
    # Comment by GOSOMI
    # @date: 2023-03-08
    def subscribe_payment_reserve_lookup(self, reserve_id=''):
        return self.__request(method='get', url=self.__entrypoints(f'subscribe/payment/reserve/{reserve_id}'))

    # cancel subscribe reserve
    # Comment by GOSOMI
    def cancel_subscribe_reserve(self, reserve_id=''):
        return self.__request(method='delete', url=self.__entrypoints(f'subscribe/payment/reserve/{reserve_id}'))

    def shipping_start(self, receipt_id='', tracking_number='', delivery_corp='', shipping_prepayment=None,
                       shipping_day=None, user=None, company=None, redirect_url=None, receipt_url=None):
        return self.__request(method='put', url=self.__entrypoints(f'escrow/shipping/start/{receipt_id}'), data={
            "tracking_number": tracking_number,
            "delivery_corp": delivery_corp,
            "shipping_prepayment": shipping_prepayment,
            "shipping_day": shipping_day,
            "user": user,
            "company": company,
            "redirect_url": redirect_url,
            "receipt_url": receipt_url,
        })

    # 현금영수증 발행
    # Comment by GOSOMI
    # @date: 2022-07-28
    def cash_receipt_publish_on_receipt(self, receipt_id='', username='', email='', phone='', identity_no='',
                                        cash_receipt_type='소득공제', currency=None):
        return self.__request(method='post', url=self.__entrypoints('request/receipt/cash/publish'), data={
            "receipt_id": receipt_id,
            "username": username,
            "email": email,
            "phone": phone,
            "identity_no": identity_no,
            "cash_receipt_type": cash_receipt_type,
            "currency": currency
        })

    # 현금영수증 취소
    # Comment by GOSOMI
    # @date: 2022-07-28
    def cash_receipt_cancel_on_receipt(self, receipt_id='', cancel_username='시스템', cancel_message='현금영수증 취소'):
        return self.__request(
            method='delete',
            url=self.__entrypoints(
                f'request/receipt/cash/cancel/{receipt_id}?'
            ),
            params=dict({
                "cancel_username": cancel_username,
                "cancel_message": cancel_message
            })
        )

    # 현금 영수증 별건 발행
    # Comment by GOSOMI
    # @date: 2022-08-09
    def request_cash_receipt(self, pg='', order_name='', identity_no='', purchased_at='', cash_receipt_type='소득공제',
                             price=0, tax_free=0, user=None, metadata=None, extra={}, order_id=''):
        return self.__request(
            method='post',
            url=self.__entrypoints('request/cash/receipt'),
            data={
                "pg": pg,
                "order_id": order_id,
                "order_name": order_name,
                "identity_no": identity_no,
                "purchased_at": purchased_at,
                "cash_receipt_type": cash_receipt_type,
                "price": price,
                "tax_free": tax_free,
                "user": user,
                "metadata": metadata,
                "extra": extra
            }
        )

    # 현금영수증 별건 발행 취소하기
    # Comment by GOSOMI
    # @date: 2022-08-09
    def cancel_cash_receipt(self, receipt_id='', cancel_username='', cancel_message=''):
        return self.__request(
            method='delete',
            url=self.__entrypoints(f'request/cash/receipt/{receipt_id}'),
            params=dict({
                "cancel_username": cancel_username,
                "cancel_message": cancel_message
            })
        )

    # 본인인증 REST API 요청
    # Comment by GOSOMI
    # @date: 2022-11-07
    def request_authentication(self, pg='', method='', username='', identity_no='', carrier='', phone='', site_url='',
                               order_name='', authentication_id='', authenticate_type='sms', client_ip='', user=None, extra={}, metadata=None):
        return self.__request(
            method='post',
            url=self.__entrypoints('request/authentication'),
            data={
                "pg": pg,
                "method": method,
                "authentication_id": authentication_id,
                "authenticate_type": authenticate_type,
                "username": username,
                "identity_no": identity_no,
                "carrier": carrier,
                "phone": phone,
                "client_ip": client_ip,
                "site_url": site_url,
                "order_name": order_name,
                "user": user,
                "extra": extra,
                "metadata": metadata
            }
        )

    # 본인인증 승인 REST API
    # Comment by GOSOMI
    # @date: 2022-11-07
    def confirm_authentication(self, receipt_id='', otp=''):
        return self.__request(
            method='post',
            url=self.__entrypoints('authenticate/confirm'),
            data={
                "receipt_id": receipt_id,
                "otp": otp
            }
        )

    # SMS로 본인인증 요청시 SMS 재발송 로직
    # Comment by GOSOMI
    # @date: 2022-11-07
    def realarm_authentication(self, receipt_id=''):
        return self.__request(
            method='post',
            url=self.__entrypoints('authenticate/realarm'),
            data={
                "receipt_id": receipt_id
            }
        )

    # 계좌 자동 결제를 위한 빌링키 발급
    def request_subscribe_automatic_transfer_billing_key(self, pg='', order_name='', price=None, tax_free=None, subscription_id='',
                                                         method=None, extra=None, user=None, metadata=None, auth_type='ARS', username='',
                                                         bank_name='', bank_account='', identity_no='', cash_receipt_type='소득공제',
                                                         cash_receipt_identity_no=None, phone=''):
        return self.__request(method='post', url=self.__entrypoints('request/subscribe/automatic-transfer'), data={
            "pg": pg,
            "order_name": order_name,
            "subscription_id": subscription_id,
            "method": method,
            "price": price,
            "tax_free": tax_free,
            "extra": extra,
            "user": user,
            "metadata": metadata,
            "auth_type": auth_type,
            "username": username,
            "bank_name": bank_name,
            "bank_account": bank_account,
            "identity_no": identity_no,
            "cash_receipt_type": cash_receipt_type,
            "cash_receipt_identity_no": cash_receipt_identity_no,
            "phone": phone,
        })


    # 출금 동의 확인 요청
    def publish_automatic_transfer_billing_key(self, receipt_id=''):
        return self.__request(method='post', url=self.__entrypoints('request/subscribe/automatic-transfer/publish'), data={
            "receipt_id": receipt_id
        })

    # 사용자 지갑 목록 조회
    def get_user_wallets(self, user_id='', sandbox=False):
        """
        .. deprecated::
            다음 메이저 버전에서 제거 예정. wallet 엔드포인트는 폐기 예정이며,
            결제는 Request::PaymentController#create 의 wallet_id + user_token 으로 처리됩니다.
        """
        warnings.warn(
            "get_user_wallets is deprecated and will be removed in a future major version.",
            DeprecationWarning,
            stacklevel=2,
        )
        sandbox_str = 'true' if sandbox else 'false'
        return self.__request(method='get', url=self.__entrypoints(f'wallet?user_id={user_id}&sandbox={sandbox_str}'))

    # 지갑 결제 요청
    def request_wallet_payment(self, user_id='', order_name='', price=0, order_id='', sandbox=False, tax_free=0,
                               webhook_url=None, content_type=None, items=None, user=None, extra=None, metadata=None):
        """
        .. deprecated::
            다음 메이저 버전에서 제거 예정. wallet 엔드포인트는 폐기 예정이며,
            결제는 wallet_id + user_token 흐름으로 전환하세요.
        """
        warnings.warn(
            "request_wallet_payment is deprecated and will be removed in a future major version.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.__request(method='post', url=self.__entrypoints('wallet/payment'), data={
            "user_id": user_id,
            "order_name": order_name,
            "price": price,
            "tax_free": tax_free,
            "order_id": order_id,
            "sandbox": sandbox,
            "webhook_url": webhook_url,
            "content_type": content_type,
            "items": items,
            "user": user,
            "extra": extra,
            "metadata": metadata
        })
