from order.enums import ReserveType, OrderStatus
from order.models import Order


class CryptoMyOrderService:
    def __init__(self, order: Order = Order):
        self.order = order

    def get(self, user):
        return self.order.objects.filter(
            user=user,
            reserve_type=ReserveType.RESERVE,
            status=OrderStatus.PENDING
        ).prefetch_related("market")