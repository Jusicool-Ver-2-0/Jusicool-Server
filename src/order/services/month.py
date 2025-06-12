from django.db.models import Sum
from django.utils import timezone

from order.enums import OrderStatus, OrderType
from order.models import Order


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