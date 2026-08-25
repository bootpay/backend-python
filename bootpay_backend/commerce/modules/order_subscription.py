import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import urlencode

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceOrderSubscription,
    OrderSubscriptionListParams,
    OrderSubscriptionUpdateParams,
    OrderSubscriptionPauseParams,
    OrderSubscriptionResumeParams,
    OrderSubscriptionPurchaseParams,
    OrderSubscriptionTransferParams,
    OrderSubscriptionTerminationParams,
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
        POST /v1/order_subscriptions/requests/ing/pause
        :param params: 일시정지 파라미터
        :return: CommerceOrderSubscription
        """
        payload, idempotency_key = self._split_idempotency(params)
        return self._bootpay.post(
            'order_subscriptions/requests/ing/pause',
            payload,
            headers=self._user_headers(idempotency_key)
        )

    def resume(self, params: OrderSubscriptionResumeParams):
        """
        정기구독 재개
        PUT /v1/order_subscriptions/requests/ing/resume
        ⚠️ requests/ing 계열 중 유일하게 PUT 이다. 오타로 보고 POST 로 바꾸지 말 것.
        :param params: 재개 파라미터
        :return: CommerceOrderSubscription
        """
        payload, idempotency_key = self._split_idempotency(params)
        return self._bootpay.put(
            'order_subscriptions/requests/ing/resume',
            payload,
            headers=self._user_headers(idempotency_key)
        )

    def purchase(self, params: OrderSubscriptionPurchaseParams):
        """
        중도인수 요청
        POST /v1/order_subscriptions/requests/ing/purchase
        :param params: 중도인수 파라미터
        :return: CommerceOrderSubscription
        """
        payload, idempotency_key = self._split_idempotency(params)
        return self._bootpay.post(
            'order_subscriptions/requests/ing/purchase',
            payload,
            headers=self._user_headers(idempotency_key)
        )

    def transfer(self, params: OrderSubscriptionTransferParams):
        """
        구독 이전/승계 요청
        POST /v1/order_subscriptions/requests/ing/transfer
        :param params: 이전/승계 파라미터
        :return: CommerceOrderSubscription
        """
        payload, idempotency_key = self._split_idempotency(params)
        return self._bootpay.post(
            'order_subscriptions/requests/ing/transfer',
            payload,
            headers=self._user_headers(idempotency_key)
        )

    def calculate_termination_fee(
        self,
        order_subscription_id: Optional[str] = None,
        order_number: Optional[str] = None,
        idempotency_key: Optional[str] = None
    ):
        """
        해지 수수료 계산
        GET /v1/order_subscriptions/requests/ing/calculate_termination_fee
        :param order_subscription_id: 정기구독 ID (선택)
        :param order_number: 주문번호 (선택)
        :param idempotency_key: 미지정시 자동 생성
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
            f'order_subscriptions/requests/ing/calculate_termination_fee?{urlencode(query_params)}',
            headers=self._user_headers(idempotency_key)
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
        POST /v1/order_subscriptions/requests/ing/termination
        :param params: 해지 파라미터
        :return: CommerceOrderSubscription
        """
        payload, idempotency_key = self._split_idempotency(params)
        return self._bootpay.post(
            'order_subscriptions/requests/ing/termination',
            payload,
            headers=self._user_headers(idempotency_key)
        )

    def _split_idempotency(self, params: Optional[Dict[str, Any]]):
        """params 에서 idempotency_key 를 분리하고 None 값을 제거한 payload 를 만든다."""
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return payload, idempotency_key

    def _user_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        requests/ing 요청 헤더 — 구매자가 올리는 요청이므로 user scope 다.
        Idempotency-Key 는 미지정시 매 호출마다 생성된다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'user'
        }


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
            if params.get('search_date_from'):
                query_params['search_date_from'] = params['search_date_from']
            if params.get('search_date_to'):
                query_params['search_date_to'] = params['search_date_to']
            if params.get('s_at'):
                query_params['s_at'] = params['s_at']
            if params.get('e_at'):
                query_params['e_at'] = params['e_at']
            if params.get('request_type'):
                query_params['request_type'] = params['request_type']
            if params.get('user_group_id'):
                query_params['user_group_id'] = params['user_group_id']
            if params.get('status') is not None:
                query_params['status'] = params['status']
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
        구독 계약 내용 변경
        PUT /v1/order_subscriptions/{order_subscription_id}
        바뀐 값만 보내면 된다 (나머지는 서버가 그대로 유지한다). supervisor scope.

        price 는 회차별 결제 금액의 기준금액이다. 바꾸면 결제예정(READY) 회차의 청구액이
        즉시 다시 계산되고, 이후 회차도 이 금액으로 만들어진다. 이미 결제된 회차는 그대로다.
        0 이하는 받지 않는다. 특정 회차만 가감하려면 order_subscription_adjustment.create 를 쓴다.
        (관리자 화면의 금액 변경과 같은 구현을 탄다)
        :param params: 수정 파라미터
        :return: CommerceOrderSubscription
        """
        if not params.get('order_subscription_id'):
            raise ValueError('order_subscription_id is required')
        params = dict(params)
        order_subscription_id = params.pop('order_subscription_id')
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'order_subscriptions/{order_subscription_id}',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def supervisor_approve(
        self,
        order_subscription_id: str,
        params: Optional[SupervisorOrderSubscriptionApproveParams] = None
    ):
        """
        관리자 정기구독 승인
        PUT /v1/order_subscriptions/{order_subscription_id}/approve
        ⚠️ 서버가 supervisor scope 를 요구한다 (scope_invalid!).
        :param order_subscription_id: 정기구독 ID
        :param params: 승인 파라미터
        :return: CommerceOrderSubscription
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'order_subscriptions/{order_subscription_id}/approve',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def supervisor_reject(
        self,
        order_subscription_id: str,
        params: Optional[SupervisorOrderSubscriptionRejectParams] = None
    ):
        """
        관리자 정기구독 거절
        PUT /v1/order_subscriptions/{order_subscription_id}/reject
        ⚠️ 서버가 supervisor scope 를 요구한다 (scope_invalid!).
        :param order_subscription_id: 정기구독 ID
        :param params: 거절 파라미터
        :return: CommerceOrderSubscription
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'order_subscriptions/{order_subscription_id}/reject',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def supervisor_terminate(
        self,
        order_subscription_id: str,
        params: Optional[SupervisorOrderSubscriptionTerminateParams] = None
    ):
        """
        관리자 정기구독 해지
        PUT /v1/order_subscriptions/{order_subscription_id}/terminate
        ⚠️ 서버가 supervisor scope 를 요구한다 (scope_invalid!).
        :param order_subscription_id: 정기구독 ID
        :param params: 해지 파라미터
        :return: CommerceOrderSubscription
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'order_subscriptions/{order_subscription_id}/terminate',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def supervisor_pause(
        self,
        order_subscription_id: str,
        params: SupervisorOrderSubscriptionPauseParams
    ):
        """
        관리자 정기구독 일시정지
        PUT /v1/order_subscriptions/{order_subscription_id}/pause
        ⚠️ 서버가 supervisor scope 를 요구한다 (scope_invalid!).
        :param order_subscription_id: 정기구독 ID
        :param params: 일시정지 파라미터
        :return: CommerceOrderSubscription
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'order_subscriptions/{order_subscription_id}/pause',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def supervisor_resume(
        self,
        order_subscription_id: str,
        params: Optional[SupervisorOrderSubscriptionResumeParams] = None
    ):
        """
        관리자 정기구독 재개
        PUT /v1/order_subscriptions/{order_subscription_id}/resume
        ⚠️ 서버가 supervisor scope 를 요구한다 (scope_invalid!).
        :param order_subscription_id: 정기구독 ID
        :param params: 재개 파라미터
        :return: CommerceOrderSubscription
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.put(
            f'order_subscriptions/{order_subscription_id}/resume',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def supervisor_charge(self, params: SupervisorOrderSubscriptionChargeParams):
        """
        수시결제(온디맨드) charge_key 즉시 결제
        POST /v1/order_subscriptions/charge (supervisor 전용)
        charge_key 는 body 로만 전송한다 (URL/query 금지 — 액세스 로그 노출 방지)
        :param params: 결제 파라미터
        :return: OrderSubscriptionChargeResponse
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.post(
            'order_subscriptions/charge',
            payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def supervisor_charge_revoke(self, params: SupervisorOrderSubscriptionChargeRevokeParams):
        """
        수시결제(온디맨드) charge_key 해지
        DELETE /v1/order_subscriptions/charge (supervisor 전용)
        해지 이후 해당 키로의 재결제는 불가능하다. 대상 charge_key 는 body 로 전송한다.
        :param params: 해지 파라미터
        :return: OrderSubscriptionChargeRevokeResponse
        """
        params = dict(params or {})
        idempotency_key = params.pop('idempotency_key', None)
        payload = {k: v for k, v in params.items() if v is not None}
        return self._bootpay.delete(
            'order_subscriptions/charge',
            data=payload,
            headers=self._supervisor_headers(idempotency_key)
        )

    def _supervisor_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """
        supervisor 전용 요청 헤더
        Idempotency-Key 는 미지정시 매 호출마다 생성된다.
        """
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }
