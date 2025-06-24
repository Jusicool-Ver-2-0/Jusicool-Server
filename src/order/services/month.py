from datetime import date, time, datetime

from django.db.models import Sum
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
            status=OrderStatus.COMPLETED
        )

        sell_price = order.filter(order_type=OrderType.SELL).aggregate(Sum("price"))
        buy_price = order.filter(order_type=OrderType.BUY).aggregate(Sum("price"))

        rate = sell_price.get("price__sum") or 0 - buy_price.get("price__sum") or 0

        return {
            "rate": rate,
            "order_count": order.count()
        }

    def get_month_rate(self, user):
        today = date.today()
        start = date(today.year, today.month, 1)
        end = datetime.combine(today, time.max)

        month_order = Order.objects.filter(
            user=user,
            created_at__gte=start,
            created_at__lte=end,
            status=OrderStatus.COMPLETED
        )

        sold_markets = month_order.filter(order_type=OrderType.SELL).values_list('market_id', flat=True).distinct()

        completed_orders = month_order.filter(market_id__in=sold_markets)

        if not completed_orders:
            raise NotFountOrderException()

        buy_price = completed_orders.filter(
            order_type=OrderType.BUY
        ).aggregate(
            sum=Sum('price')
        ).get('sum') or 0

        sell_price = completed_orders.filter(
            order_type=OrderType.SELL
        ).aggregate(
            sum=Sum('price')
        ).get('sum') or 0

        if buy_price == 0:
            rate = 0
        else:
            rate = ((sell_price - buy_price) / buy_price) * 100

        market_rates = []
        for market_id in sold_markets:
            market_orders = completed_orders.filter(market_id=market_id)

            market_buy_price = market_orders.filter(
                order_type=OrderType.BUY
            ).aggregate(
                sum=Sum('price')
            ).get('sum') or 0

            market_sell_price = market_orders.filter(
                order_type=OrderType.SELL
            ).aggregate(
                sum=Sum('price')
            ).get('sum') or 0

            if market_buy_price > 0:
                m_rate = ((market_sell_price - market_buy_price) / market_buy_price) * 100
            else:
                m_rate = 0

            market_obj = market_orders.first().market

            market_rates.append({
                'market': market_obj.market,
                'korean_name': market_obj.korean_name,
                'rate': round(m_rate, 2)
            })

        return MonthlyRateSerializer(
            {
                'monthly_rate': round(rate, 2),
                'markets': market_rates
            }
        )