from decimal import Decimal

import requests
from django.conf import settings

from exchange.enums import ExchangeType
from exchange.exceptions import ShortageUSDBalanceException
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

    def exchange(self, user, exchange_type: ExchangeType, data: ExchangeSerializer):
        if exchange_type == ExchangeType.KRW.value:
            self._to_krw(user, data)
        elif exchange_type == ExchangeType.USD.value:
            self._to_usd(user, data)

    def _to_krw(self, user, data: ExchangeSerializer):
        user_account = self.account.objects.get(user=user)

        exchange_rate = requests.get(
            f"{settings.EXCHANGE_API_BASE_URL}/latest/USD"
        )
        krw_exchange_rate = exchange_rate.json().get("rates").get("KRW")

        decrease_usd = data.get("amount")
        increase_krw = int(data.get("amount") * krw_exchange_rate)

        if user_account.usd_balance < decrease_usd:
            raise ShortageUSDBalanceException()

        # Account 데이터 저장
        user_account.usd_balance -= Decimal(decrease_usd)
        user_account.krw_balance += increase_krw
        user_account.save()

        # Account history 기록
        self.account_history.save(
            AccountHistory(
                account=user_account,
                changed_usd=-decrease_usd,
                changed_krw=increase_krw
            )
        )

    def _to_usd(self, data: ExchangeSerializer):
        pass
