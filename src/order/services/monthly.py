import time
from datetime import date, datetime, time
from django.db.models import Sum

from order.enums import OrderStatus, OrderType
from order.exceptions import NotFountOrderException
from order.models import Order
from order.serializers import MonthlyPercentSerializer


class MonthlyService:
    def get_monthly_percent(self, user):

        today = date.today()
        start = date(today.year, today.month, 1)
        end = datetime.combine(today, time.max)

        month_order = Order.objects.filter(
            user=user,
            created_at__gte=start,
            created_at__lte=end,
            status=OrderStatus.COMPLETED
        )

        sold_markets = month_order.filter(order_type=OrderType.SELL).values_list('market_id', flat=True)

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

        return MonthlyPercentSerializer(
            {
                'rate': round(rate, 2)
            }
        )