from django.db import transaction
from django.shortcuts import get_object_or_404

from account.models import Account
from holding.models import Holding
from market.models import Market
from order.enums import OrderType, ReserveType, OrderStatus
from order.exceptions import ShortageKRWBalanceException, InvalidQuantityException
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
    def buy(self, user, serializer: MarketReserveOrderSerializer, market: str):
        user_account = get_object_or_404(Account, user=user)
        market = get_object_or_404(Market, market=market)

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
            reserve_price=serializer.validated_data.get("price"),
            status=OrderStatus.PENDING,
        )
        order.save()

    @transaction.atomic
    def sell(self, user, serializer: MarketReserveOrderSerializer, market: str):
        market = get_object_or_404(Market, market=market)
        user_holding = get_object_or_404(Holding, user=user, market=market.id)

        if user_holding.quantity < serializer.validated_data.get("quantity"):
            raise InvalidQuantityException()

        order = Order(
            user=user,
            market=market,
            order_type=OrderType.SELL,
            reserve_type=ReserveType.RESERVE,
            quantity=serializer.validated_data.get("quantity"),
            execute_price=serializer.validated_data.get("price"),
            status=OrderStatus.PENDING,
        )
        order.save()
