import uuid
from typing import TYPE_CHECKING, Optional, Dict, Any
from urllib.parse import quote

if TYPE_CHECKING:
    from ..commerce_resource import BootpayCommerceResource

from ..types import (
    CommerceDeposit,
    DepositAccountsResponse,
    DepositCreateParams,
    DepositWebhookSecretResponse
)


class DepositModule:
    """
    뱅크알람 입금대기 모듈 (/v1/sdk/deposits)

    판매자 폰의 입금 알림 중 금액·입금자명이 맞는 것을 주문에 연결하고 입금 웹훅으로 알린다.
    인스턴스 role 과 무관하게 모든 요청은 supervisor 전용이다.
    """

    def __init__(self, bootpay: 'BootpayCommerceResource'):
        self._bootpay = bootpay

    def accounts(self) -> DepositAccountsResponse:
        """
        판매자 입금 계좌 목록
        GET /v1/sdk/deposits/accounts
        첫 계좌가 대표 계좌(primary: True)다.
        :return: {'accounts': List[DepositAccount]}
        """
        return self._bootpay.get('sdk/deposits/accounts', headers=self._supervisor_headers())

    def webhook_secret(self, idempotency_key: Optional[str] = None) -> DepositWebhookSecretResponse:
        """
        웹훅 서명 비밀값 발급
        POST /v1/sdk/deposits/webhook_secret
        ⚠️ 원문은 이 응답에서만 준다. 다시 부르면 바뀐다 (기존 웹훅 작업은 이전 비밀값으로 서명된다).
        :param idempotency_key: 미지정시 자동 생성
        :return: {'secret': str}
        """
        return self._bootpay.post(
            'sdk/deposits/webhook_secret', {},
            headers=self._supervisor_headers(idempotency_key)
        )

    def create(self, params: DepositCreateParams) -> CommerceDeposit:
        """
        입금대기 등록
        POST /v1/sdk/deposits
        같은 merchant_order_id 재호출은 기존 주문을 반환한다 (금액·입금자명·계좌가 다르면 18110).
        webhook_url 을 주려면 webhook_secret() 으로 비밀값을 먼저 발급받아야 한다 (18131).
        notify 는 유료 알림톡이며, 준비가 안 됐으면 주문을 만들지 않는다 (18133).
        :param params: merchant_order_id · price · depositor 필수, idempotency_key 선택
        :return: CommerceDeposit
        """
        payload = self._compact({k: v for k, v in params.items() if k != 'idempotency_key'})
        if payload.get('notify') is not None:
            payload['notify'] = self._compact(payload['notify'])
        return self._bootpay.post(
            'sdk/deposits', payload,
            headers=self._supervisor_headers(params.get('idempotency_key'))
        )

    def detail(self, deposit_id: str) -> CommerceDeposit:
        """
        입금대기 조회
        GET /v1/sdk/deposits/{id}
        기한이 지났으면 조회 시점에 만료(expired)로 닫힌다.
        :param deposit_id: 가맹점 주문번호 또는 부트페이 주문번호
        :return: CommerceDeposit
        """
        if not deposit_id:
            raise ValueError('deposit_id is required')
        return self._bootpay.get(
            f'sdk/deposits/{quote(deposit_id, safe="")}',
            headers=self._supervisor_headers()
        )

    def cancel(self, deposit_id: str, idempotency_key: Optional[str] = None) -> CommerceDeposit:
        """
        입금대기 취소
        DELETE /v1/sdk/deposits/{id}
        기한이 지났으면 만료로 닫고, 이미 닫힌 주문은 그대로 반환한다. 입금 확인된 주문은 18108.
        :param deposit_id: 가맹점 주문번호 또는 부트페이 주문번호
        :param idempotency_key: 미지정시 자동 생성
        :return: CommerceDeposit
        """
        if not deposit_id:
            raise ValueError('deposit_id is required')
        return self._bootpay.delete(
            f'sdk/deposits/{quote(deposit_id, safe="")}',
            headers=self._supervisor_headers(idempotency_key)
        )

    def _compact(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """None 값을 제거한다 (False 는 남긴다)."""
        return {k: v for k, v in payload.items() if v is not None}

    def _supervisor_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        """요청별 supervisor 헤더와 멱등키 (미지정시 매 호출마다 UUID 생성)."""
        return {
            'Idempotency-Key': idempotency_key or str(uuid.uuid4()),
            'BOOTPAY-ROLE': 'supervisor'
        }
