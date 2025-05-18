from order.enums import ReserveType, OrderStatus
from order.models import Order


class CryptoMyOrderService:
    def __init__(
            self,
            order: Order = Order,
    ):
        self.order = order

    def get(self, user, order_type):
        if order_type == "reserve":
            return self.order.objects.filter(
                user=user,
                reserve_type=ReserveType.RESERVE,
                status=OrderStatus.PENDING
            ).prefetch_related("market")
        elif order_type == "completed":
            return self.order.objects.filter(
                user=user,
                status=OrderStatus.COMPLETED
            ).prefetch_related("market")
        else:
            return self.order.objects.filter(
                user=user,
            ).prefetch_related("market")