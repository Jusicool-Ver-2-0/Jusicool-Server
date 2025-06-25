import requests
from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404

from account.enums import AccountHistoryType
from account.models import Account, AccountHistory
from holding.models import Holding
from market.enums import MarketType
from order.enums import OrderType, ReserveType, OrderStatus
from order.exceptions import TradePriceFetchException, ShortageKRWBalanceException, InvalidQuantityException
from order.models import Order


@shared_task
@transaction.atomic
def crypto_reserve_sell_task():
    # reserve buy order 조회
    reserve_buy_order = Order.objects.filter(
        order_type=OrderType.SELL,
        reserve_type=ReserveType.RESERVE,
        status=OrderStatus.PENDING
    )
    if not reserve_buy_order:
        return

    markets = ",".join([str(m.market.market) for m in reserve_buy_order])

    crypto_trade_price = requests.get(
        f"{settings.CRYPTO_API_BASE_URL}/ticker",
        params={"markets": markets},
    )
    if crypto_trade_price.status_code != 200:
        raise TradePriceFetchException()

    # 검색 최적화를 위한 인덱스
    crypto_trade_price_index = {c.get("market"): c for c in crypto_trade_price.json()}

    for order in reserve_buy_order:
        # order.market 의 현재가 파싱
        trade_price = crypto_trade_price_index.get(order.market.market).get("trade_price")

        # 예약 채결 조건이 아닌경우 pass
        if trade_price < order.reserve_price:
            continue

        order.status = OrderStatus.COMPLETED
        order.save()

        increase_krw = trade_price * order.quantity

        # 계좌 조회
        user_account = get_object_or_404(Account, user=order.user)

        user_account.krw_balance += increase_krw
        user_account.save()

        AccountHistory(
            account=user_account,
            order=order,
            history_type=AccountHistoryType.ORDER,
            changed_krw=increase_krw,
        ).save()

        # 홀딩 quantity 변경 or delete
        holding = Holding.objects.filter(
            user=order.user,
            market=order.market,
            market_type=MarketType.CRYPTO,
        ).first()

        if holding.quantity < order.quantity:
            continue
        elif holding.quantity == order.quantity:
            holding.delete()
            continue
        elif holding.quantity > order.quantity:
            holding.quantity -= order.quantity

        holding.save()
