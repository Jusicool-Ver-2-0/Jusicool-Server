from django.db import transaction
from django.shortcuts import get_object_or_404

from account.enums import AccountHistoryType
from account.models import Account, AccountHistory
from holding.models import Holding
from market.models import Market
from order.enums import OrderType, OrderStatus, ReserveType
from order.exceptions import ShortageKRWBalanceException, InvalidQuantityException
from order.models import Order
from order.serializers import MarketOrderSerializer, OrderPriceSerializer
from order.services.order import OrderService


class ImmediatelyOrderServiceImpl(OrderService):
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
    def buy(self, user, serializer: MarketOrderSerializer, market: str):
        user_account = get_object_or_404(Account, user=user)  # 사용자 계좌
        market = get_object_or_404(Market, market=market)  # 마켓 정보
        quantity = serializer.validated_data.get("quantity")  # 주문 수량

        trade_price, price = self._calculate_price(
            market=market.market,
            quantity=quantity,
            market_type=market.market_type
        )

        if user_account.krw_balance < price:
            raise ShortageKRWBalanceException()

        # 계좌 잔고 감소
        user_account.krw_balance -= price
        user_account.save()

        # 주문 생성
        order = Order(
            user=user,
            market=market,
            order_type=OrderType.BUY,
            reserve_type=ReserveType.IMMEDIATE,
            quantity=quantity,
            reserve_price=trade_price,
            status=OrderStatus.COMPLETED,
        )
        order.save()

        # 홀딩 조회
        exists_holding = self.holding.objects.filter(
            user=user,
            market=market,
            market_type=market.market_type,
        ).first()

        if exists_holding:  # 현재가에 홀딩이 존재한다면 평균값 계산 후 수량 증가
            exists_holding.price = (exists_holding.price + trade_price) / 2
            exists_holding.quantity += quantity
            exists_holding.save()

        else:  # 새로운 홀딩 생성
            Holding(
                user=user,
                market=market,
                quantity=quantity,
                market_type=market.market_type,
                price=trade_price,
            ).save()

        # 계좌 히스토리 기록
        account_history = AccountHistory(
            account=user_account,
            order=order,
            history_type=AccountHistoryType.ORDER,
            changed_krw=-price,
            changed_usd=0
        )
        account_history.full_clean()
        account_history.save()

        return OrderPriceSerializer({'price': price}).data

    @transaction.atomic
    def sell(self, user, serializer: MarketOrderSerializer, market: str):
        user_account = get_object_or_404(Account, user=user)
        market = get_object_or_404(Market, market=market)
        user_holding = get_object_or_404(Holding, user=user, market=market)
        quantity = serializer.validated_data.get("quantity")

        if user_holding.quantity < quantity:
            raise InvalidQuantityException()

        trade_price, price = self._calculate_price(market.market, quantity=quantity, market_type=market.market_type)

        user_account.krw_balance += price
        user_account.save()

        order = Order(
            user=user,
            market=market,
            order_type=OrderType.SELL,
            reserve_type=ReserveType.IMMEDIATE,
            quantity=quantity,
            reserve_price=trade_price,
            status=OrderStatus.COMPLETED,
        )
        order.save()

        if user_holding.quantity == quantity:
            user_holding.delete()
        else:
            user_holding.quantity -= quantity
            user_holding.save()

        account_history = AccountHistory(
            account=user_account,
            order=order,
            history_type=AccountHistoryType.ORDER,
            changed_krw=price,
            changed_usd=0
        )
        account_history.full_clean()
        account_history.save()

        return OrderPriceSerializer({'price': price}).data