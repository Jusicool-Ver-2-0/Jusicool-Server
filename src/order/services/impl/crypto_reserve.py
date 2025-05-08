import requests
from django.conf import settings
from django.db import transaction

from account.models import Account
from holding.models import Holding
from market.models import Market
from order.enums import OrderType, ReserveType, OrderStatus
from order.exceptions import ShortageKRWBalanceException, InvalidQuantityException, TradePriceFetchException
from order.models import Order
from order.serializers import MarketReserveOrderSerializer
from order.services.reserve import ReserveOrderService


class CryptoReserveOrderServiceImpl(ReserveOrderService):
    def __init__(
            self,
            account: Account = Account,
            market: Market = Market,
            holding: Holding = Holding
    ):
        self.account = account
        self.market = market
        self.holding = holding

    @transaction.atomic
    def reserve_buy(self, user, serializer: MarketReserveOrderSerializer, market_id: int):
        user_account = self.account.objects.get(user=user)
        market = Market.objects.get(id=market_id)

        trade_price, price = self._calculate_price(market.market, quantity=serializer.validated_data.get("quantity"))

        if user_account.krw_balance < trade_price:
            raise ShortageKRWBalanceException()

        order = Order(
            user=user,
            order_type=OrderType.BUY.value,
            reserve_type=ReserveType.RESERVE.value,
            quantity=serializer.validated_data.get("quantity"),
            price=serializer.validated_data.get("price"),  # 예약가
            status=OrderStatus.PENDING.value,
        )
        order.save()

    @transaction.atomic
    def reserve_sell(self, user, serializer: MarketReserveOrderSerializer, market_id: int):
        market = Market.objects.get(id=market_id)
        user_holding = self.holding.objects.get(user=user, market=market.id)

        if user_holding.quantity < serializer.validated_data.get("quantity"):
            raise InvalidQuantityException()

        order = Order(
            user=user,
            order_type=OrderType.SELL.value,
            reserve_type=ReserveType.RESERVE.value,
            quantity=serializer.validated_data.get("quantity"),
            price=serializer.validated_data.get("price"),
            status=OrderStatus.PENDING.value,
        )
        order.save()

    def _fetch_trade_price(self, market: str) -> float:
        crypto_trade_price = requests.get(
            f"{settings.CRYPTO_API_BASE_URL}/ticker",
            params={"markets": market},
        )
        if crypto_trade_price.status_code != 200:
            raise TradePriceFetchException()
        return float(crypto_trade_price.json()[0].get("trade_price"))
