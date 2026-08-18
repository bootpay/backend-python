import uuid
from typing import TYPE_CHECKING, Optional
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceOrderSubscription,
    OrderSubscriptionListParams,
    OrderSubscriptionUpdateParams,
    OrderSubscriptionPauseParams,
    OrderSubscriptionResumeParams,
    OrderSubscriptionTerminationParams,
    OrderSubscriptionPurchaseParams,
    OrderSubscriptionTransferParams,
    CalcTerminateFeeResponse,
    SupervisorOrderSubscriptionApproveParams,
    SupervisorOrderSubscriptionRejectParams,
    SupervisorOrderSubscriptionTerminateParams,
    SupervisorOrderSubscriptionPauseParams,
    SupervisorOrderSubscriptionResumeParams,
    SupervisorOrderSubscriptionChargeParams,
    SupervisorOrderSubscriptionChargeRevokeParams
)


class OrderSubscriptionRequestIngModule:
    """정기구독 진행 중 요청 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def pause(self, params: OrderSubscriptionPauseParams):
        """
        정기구독 일시정지
        :param params: 일시정지 파라미터
        :return: CommerceOrderSubscription
        """
        return self._bootpay.post('order_subscriptions/requests/ing/pause', params)

    def resume(self, params: OrderSubscriptionResumeParams):
        """
        정기구독 재개
        :param params: 재개 파라미터
        :return: CommerceOrderSubscription
        """
        return self._bootpay.put('order_subscriptions/requests/ing/resume', params)

    def calculate_termination_fee(
        self,
        order_subscription_id: Optional[str] = None,
        order_number: Optional[str] = None
    ):
        """
        해지 수수료 계산
        :param order_subscription_id: 정기구독 ID (선택)
        :param order_number: 주문번호 (선택)
        :return: CalcTerminateFeeResponse
        """
        if not order_subscription_id and not order_number:
            raise ValueError('order_subscription_id or order_number is required')

        query_params = {}
        if order_subscription_id:
            query_params['order_subscription_id'] = order_subscription_id
        if order_number:
            query_params['order_number'] = order_number

        return self._bootpay.get(
            f'order_subscriptions/requests/ing/calculate_termination_fee?{urlencode(query_params)}'
        )

    def calculate_termination_fee_by_order_number(self, order_number: str):
        """
        주문번호로 해지 수수료 계산
        :param order_number: 주문번호
        :return: CalcTerminateFeeResponse
        """
        return self.calculate_termination_fee(order_number=order_number)

    def termination(self, params: OrderSubscriptionTerminationParams):
        """
        정기구독 해지
        :param params: 해지 파라미터
        :return: CommerceOrderSubscription
        """
        return self._bootpay.post('order_subscriptions/requests/ing/termination', params)

    def purchase(self, params: OrderSubscriptionPurchaseParams):
        """
        정기구독 중도인수 요청 (POST /v1/order_subscriptions/requests/ing/purchase)
        :param params: 인수 파라미터 (order_subscription_id, price, tax_free_price, reason)
        :return: CommerceOrderSubscription
        """
        return self._bootpay.post('order_subscriptions/requests/ing/purchase', params)

    def transfer(self, params: OrderSubscriptionTransferParams):
        """
        정기구독 이전/승계 요청 (POST /v1/order_subscriptions/requests/ing/transfer)
        :param params: 이전 파라미터 (order_subscription_id, new_user_id, new_username,
                       new_user_email, new_user_phone, new_user_address, wallet_id, reason)
        :return: CommerceOrderSubscription
        """
        return self._bootpay.post('order_subscriptions/requests/ing/transfer', params)


class OrderSubscriptionModule:
    """정기구독 모듈"""

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay
        self.request_ing = OrderSubscriptionRequestIngModule(bootpay)

    def list(self, params: Optional[OrderSubscriptionListParams] = None):
        """
        정기구독 목록 조회
        :param params: 조회 파라미터
        :return: {'items': List[CommerceOrderSubscription], 'total': int}
        """
        query_params = {}
        if params:
            if params.get('page') is not None:
                query_params['page'] = params['page']
            if params.get('limit') is not None:
                query_params['limit'] = params['limit']
            if params.get('keyword'):
                query_params['keyword'] = params['keyword']
            if params.get('s_at'):
                query_params['s_at'] = params['s_at']
            if params.get('e_at'):
                query_params['e_at'] = params['e_at']
            if params.get('search_date_from'):
                query_params['search_date_from'] = params['search_date_from']
            if params.get('search_date_to'):
                query_params['search_date_to'] = params['search_date_to']
            if params.get('status') is not None:
                query_params['status'] = params['status']
            if params.get('request_type'):
                query_params['request_type'] = params['request_type']
            if params.get('user_group_id'):
                query_params['user_group_id'] = params['user_group_id']
            if params.get('user_id'):
                query_params['user_id'] = params['user_id']

        query = urlencode(query_params) if query_params else ''
        return self._bootpay.get(f'order_subscriptions{"?" + query if query else ""}')

    def detail(self, order_subscription_id: str):
        """
        정기구독 상세 조회
        :param order_subscription_id: 정기구독 ID
        :return: CommerceOrderSubscription
        """
        return self._bootpay.get(f'order_subscriptions/{order_subscription_id}')

    def update(self, params: OrderSubscriptionUpdateParams):
        """
        정기구독 수정
        :param params: 수정 파라미터
        :return: CommerceOrderSubscription
        """
        if not params.get('order_subscription_id'):
            raise ValueError('order_subscription_id is required')
        return self._bootpay.put(f'order_subscriptions/{params["order_subscription_id"]}', params)

    # 진행중 요청(requests/ing) 위임 메서드
    # request_ing 모듈과 동일하게 동작한다
    def pause(self, params: OrderSubscriptionPauseParams):
        """정기구독 일시정지 요청 (request_ing.pause 위임)"""
        return self.request_ing.pause(params)

    def resume(self, params: OrderSubscriptionResumeParams):
        """정기구독 재개 요청 (request_ing.resume 위임)"""
        return self.request_ing.resume(params)

    def termination(self, params: OrderSubscriptionTerminationParams):
        """정기구독 중도해지 요청 (request_ing.termination 위임)"""
        return self.request_ing.termination(params)

    def purchase(self, params: OrderSubscriptionPurchaseParams):
        """정기구독 중도인수 요청 (request_ing.purchase 위임)"""
        return self.request_ing.purchase(params)

    def transfer(self, params: OrderSubscriptionTransferParams):
        """정기구독 이전/승계 요청 (request_ing.transfer 위임)"""
        return self.request_ing.transfer(params)

    def calculate_termination_fee(self, order_subscription_id: Optional[str] = None,
                                  order_number: Optional[str] = None):
        """중도해지 수수료 사전계산 (request_ing.calculate_termination_fee 위임)"""
        return self.request_ing.calculate_termination_fee(order_subscription_id, order_number)

    def supervisor_approve(self, order_subscription_id: str, params: Optional[SupervisorOrderSubscriptionApproveParams] = None):
        return self._bootpay.put(f'order_subscriptions/{order_subscription_id}/approve', params or {})

    def supervisor_reject(self, order_subscription_id: str, params: Optional[SupervisorOrderSubscriptionRejectParams] = None):
        return self._bootpay.put(f'order_subscriptions/{order_subscription_id}/reject', params or {})

    def supervisor_terminate(self, order_subscription_id: str, params: Optional[SupervisorOrderSubscriptionTerminateParams] = None):
        return self._bootpay.put(f'order_subscriptions/{order_subscription_id}/terminate', params or {})

    def supervisor_pause(self, order_subscription_id: str, params: SupervisorOrderSubscriptionPauseParams):
        return self._bootpay.put(f'order_subscriptions/{order_subscription_id}/pause', params)

    def supervisor_resume(self, order_subscription_id: str, params: Optional[SupervisorOrderSubscriptionResumeParams] = None):
        return self._bootpay.put(f'order_subscriptions/{order_subscription_id}/resume', params or {})

    def _supervisor_headers(self, idempotency_key: Optional[str] = None):
        """supervisor 전용 헤더 생성"""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }

    def supervisor_charge(self, params: SupervisorOrderSubscriptionChargeParams, idempotency_key: Optional[str] = None):
        """
        수시결제(온디맨드) charge_key 즉시 결제
        charge_key는 body로만 전송한다 (URL/query 금지 - 액세스 로그 노출 방지)
        :param params: 결제 파라미터 (charge_key, price, tax_free_price, user, metadata)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 결제 결과
        """
        if not params.get('charge_key'):
            raise ValueError('charge_key is required')
        payload = {key: value for key, value in params.items() if value is not None}
        return self._bootpay.post(
            'order_subscriptions/charge',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def supervisor_charge_revoke(self, params: SupervisorOrderSubscriptionChargeRevokeParams,
                                 idempotency_key: Optional[str] = None):
        """
        수시결제(온디맨드) charge_key 해지
        해지 이후 해당 키로의 재결제는 불가능하다
        :param params: 해지 파라미터 (charge_key, user)
        :param idempotency_key: 멱등키 (미지정시 자동 생성)
        :return: 해지 결과
        """
        if not params.get('charge_key'):
            raise ValueError('charge_key is required')
        payload = {key: value for key, value in params.items() if value is not None}
        return self._bootpay.delete(
            'order_subscriptions/charge',
            headers=self._supervisor_headers(idempotency_key),
            data=payload
        )
