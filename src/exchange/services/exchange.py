from decimal import Decimal

import requests
from django.conf import settings
from django.db import transaction

from account.enums import AccountHistoryType
from exchange.enums import ExchangeType
from exchange.exceptions import ShortageUSDBalanceException, ShortageKRWBalanceException
from account.models import Account, AccountHistory
from exchange.serializers import ExchangeSerializer


class ExchangeService:
    def __init__(
            self,
            account: Account = Account,
            account_history: AccountHistory = AccountHistory,
    ):
        self.account = account
        self.account_history = account_history

    @transaction.atomic
    def exchange(self, user, exchange_type: ExchangeType, data: ExchangeSerializer.validated_data):
        if exchange_type == ExchangeType.KRW.value:
            self._to_krw(user, data)
        elif exchange_type == ExchangeType.USD.value:
            self._to_usd(user, data)

    def _to_krw(self, user, data: ExchangeSerializer.validated_data):
        user_account = self.account.objects.get(user=user)
        krw_exchange_rate = self._get_krw_exchange_rate()

        # 환전
        decrease_usd = data.get("amount")
        increase_krw = int(data.get("amount") * krw_exchange_rate)

        if user_account.usd_balance < decrease_usd:
            raise ShortageUSDBalanceException()

        # Account 데이터 저장
        user_account.usd_balance -= Decimal(decrease_usd)
        user_account.krw_balance += increase_krw
        user_account.save()

        # Account history 기록
        AccountHistory(
            account=user_account,
            changed_usd=-decrease_usd,
            changed_krw=increase_krw,
            type=AccountHistoryType.EXCHANGE.value,
        ).save()

    def _to_usd(self, user, data: ExchangeSerializer.validated_data):
        user_account = self.account.objects.get(user=user)
        krw_exchange_rate = self._get_krw_exchange_rate()

        # 환전
        decrease_krw = int(data.get("amount") * krw_exchange_rate)
        increase_usd = data.get("amount")

        if user_account.krw_balance < decrease_krw:
            raise ShortageKRWBalanceException()

        # Account 데이터 저장
        user_account.usd_balance += Decimal(increase_usd)
        user_account.krw_balance -= decrease_krw
        user_account.save()

        # Account history 기록
        AccountHistory(
            account=user_account,
            changed_usd=increase_usd,
            changed_krw=-decrease_krw,
            type=AccountHistoryType.EXCHANGE.value,
        ).save()

    def _get_krw_exchange_rate(self):
        exchange_rate = requests.get(
            f"{settings.EXCHANGE_API_BASE_URL}/latest/USD"
        )
        return exchange_rate.json().get("rates").get("KRW")