import requests
from django.conf import settings
from django.db import transaction

from account.models import Account
from core.kis import kis
from holding.models import Holding
from market.enums import MarketType
from market.models import Market
from order.enums import OrderType, ReserveType, OrderStatus
from order.exceptions import ShortageKRWBalanceException, InvalidQuantityException, TradePriceFetchException
from order.models import Order
from order.serializers import MarketReserveOrderSerializer
from order.services.order import OrderService


class ReserveOrderServiceImpl(OrderService):
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
    def buy(self, user, serializer: MarketReserveOrderSerializer, market_id: int):
        user_account = self.account.objects.get(user=user)
        market = Market.objects.get(id=market_id)

        trade_price, price = self._calculate_price(
            market.market,
            quantity=serializer.validated_data.get("quantity"),
            market_type=market.market_type
        )

        if user_account.krw_balance < trade_price:
            raise ShortageKRWBalanceException()

        order = Order(
            user=user,
            market=market,
            order_type=OrderType.BUY,
            reserve_type=ReserveType.RESERVE,
            quantity=serializer.validated_data.get("quantity"),
            price=serializer.validated_data.get("price"),  # 예약가
            status=OrderStatus.PENDING,
        )
        order.save()

    @transaction.atomic
    def sell(self, user, serializer: MarketReserveOrderSerializer, market_id: int):
        market = Market.objects.get(id=market_id)
        user_holding = self.holding.objects.get(user=user, market=market.id)

        if user_holding.quantity < serializer.validated_data.get("quantity"):
            raise InvalidQuantityException()

        order = Order(
            user=user,
            market=market,
            order_type=OrderType.SELL,
            reserve_type=ReserveType.RESERVE,
            quantity=serializer.validated_data.get("quantity"),
            price=serializer.validated_data.get("price"),
            status=OrderStatus.PENDING,
        )
        order.save()
