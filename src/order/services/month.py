from datetime import date, time, datetime

from django.db.models import Sum, QuerySet
from django.shortcuts import get_list_or_404
from django.utils import timezone

from order.enums import OrderStatus, OrderType
from order.exceptions import NotFountOrderException
from order.models import Order
from order.serializers import MonthlyRateSerializer


class MonthOrderService:
    def __init__(self, order: Order = Order):
        self.order = order

    def get_month_orders(self, user):
        order = self.order.objects.filter(
            user=user,
            created_at__gte=timezone.now().replace(day=1),
            created_at__lte=timezone.now(),
            status=OrderStatus.COMPLETED,
        )

        sell_price = order.filter(order_type=OrderType.SELL).aggregate(
            Sum("execute_price")
        )
        buy_price = order.filter(order_type=OrderType.BUY).aggregate(
            Sum("execute_price")
        )

        rate = sell_price.get("execute_price__sum", 0) - buy_price.get(
            "execute_price__sum", 0
        )

        return {"rate": rate, "order_count": order.count()}

    def get_month_rate(self, user):
        today = date.today()
        start = date(today.year, today.month, 1)
        end = datetime.combine(today, time.max)

        month_orders = Order.objects.filter(
            user=user,
            created_at__gte=start,
            created_at__lte=end,
            status=OrderStatus.COMPLETED,
        )

        sold_markets = (
            month_orders.filter(order_type=OrderType.SELL)
            .values_list("market_id", flat=True)
            .distinct()
        )
        completed_orders = month_orders.filter(market_id__in=sold_markets)
        if not completed_orders.exists():
            raise NotFountOrderException()

        buy_price = self._agg_sum(completed_orders, OrderType.BUY)
        sell_price = self._agg_sum(completed_orders, OrderType.SELL)
        rate = ((sell_price - buy_price) / buy_price) * 100 if buy_price else 0

        market_rates = []
        for market_id in sold_markets:
            market_orders = completed_orders.filter(market_id=market_id)
            market_buy = self._agg_sum(market_orders, OrderType.BUY)
            market_sell = self._agg_sum(market_orders, OrderType.SELL)
            m_rate = (
                ((market_sell - market_buy) / market_buy) * 100 if market_buy else 0
            )
            market_obj = market_orders.first().market
            market_rates.append(
                {
                    "market": market_obj.market,
                    "korean_name": market_obj.korean_name,
                    "rate": round(m_rate, 2),
                    "proceed": market_sell - market_buy,
                    "day": market_obj.updated_at,
                }
            )

        return MonthlyRateSerializer(
            {"monthly_rate": round(rate, 2), "markets": market_rates}
        )

    def _agg_sum(self, qs: QuerySet, order_type: str):
        f = qs.filter(order_type=order_type)
        a = f.aggregate(sum=Sum("execute_price"))
        return a.get("sum") or 0
