import requests
from django.conf import settings
from django.db import transaction

from account.enums import AccountHistoryType
from account.models import Account, AccountHistory
from holding.models import Holding
from market.enums import MarketType
from market.models import Market
from order.enums import OrderType, OrderStatus, ReserveType
from order.exceptions import ShortageKRWBalanceException, InvalidQuantityException, TradePriceFetchException
from order.models import Order
from order.serializers import MarketOrderSerializer
from order.services.order import OrderService


class CryptoOrderServiceImpl(OrderService):
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
    def buy(self, user, serializer: MarketOrderSerializer, market_id: int):
        user_account = self.account.objects.get(user=user)
        market = Market.objects.get(id=market_id)

        trade_price, price = self._calculate_price(market.market, quantity=serializer.validated_data.get("quantity"))

        if user_account.krw_balance < price:
            raise ShortageKRWBalanceException()

        # 계좌 잔고 감소
        user_account.krw_balance -= price
        user_account.save()

        # 주문 생성
        order = Order(
            user=user,
            order_type=OrderType.BUY.value,
            reserve_type=ReserveType.NOW.value,
            quantity=serializer.validated_data.get("quantity"),
            price=trade_price,
            status=OrderStatus.COMPLETED.value,
        )
        order.save()

        # 홀딩 조회
        exists_holding = Holding.objects.filter(
            user=user,
            market=market,
            type=MarketType.CRYPTO.value,
        ).first()
        if exists_holding:  # 현재가에 홀딩이 존재한다면 평균값 계산 후 수량 증가
            exists_holding.price = (exists_holding.price + trade_price) / 2
            exists_holding.quantity += serializer.validated_data.get("quantity")
            exists_holding.save()

        else:  # 새로운 홀딩 생성
            Holding(
                user=user,
                market=market,
                quantity=serializer.validated_data.get("quantity"),
                type=MarketType.CRYPTO.value,
                price=trade_price,
            ).save()

        # 계좌 히스토리 기록
        account_history = AccountHistory(
            account=user_account,
            order=order,
            history_type=AccountHistoryType.ORDER.value,
            changed_krw=-price,
            changed_usd=0
        )
        account_history.full_clean()
        account_history.save()

    @transaction.atomic
    def sell(self, user, serializer: MarketOrderSerializer, market_id: int):
        user_account = self.account.objects.get(user=user)
        market = self.market.objects.get(id=market_id)
        user_holding = self.holding.objects.get(user=user, market=market)

        if user_holding.quantity < serializer.validated_data.get("quantity"):
            raise InvalidQuantityException()

        trade_price, price = self._calculate_price(market.market, quantity=serializer.validated_data.get("quantity"))

        user_account.krw_balance += price
        user_account.save()

        order = Order(
            user=user,
            order_type=OrderType.SELL.value,
            reserve_type=ReserveType.NOW.value,
            quantity=serializer.validated_data.get("quantity"),
            price=trade_price,
            status=OrderStatus.COMPLETED.value,
        )
        order.save()

        if user_holding.quantity == serializer.validated_data.get("quantity"):
            user_holding.delete()
        else:
            user_holding.quantity -= serializer.validated_data.get("quantity")
            user_holding.save()

        account_history = AccountHistory(
            account=user_account,
            order=order,
            history_type=AccountHistoryType.ORDER.value,
            changed_krw=price,
            changed_usd=0
        )
        account_history.full_clean()
        account_history.save()

    def _fetch_trade_price(self, market: str) -> float:
        crypto_trade_price = requests.get(
            f"{settings.CRYPTO_API_BASE_URL}/ticker",
            params={"markets": market},
        )
        if crypto_trade_price.status_code != 200:
            raise TradePriceFetchException()
        return float(crypto_trade_price.json()[0].get("trade_price"))
