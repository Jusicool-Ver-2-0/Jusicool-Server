from market.enums import MarketType
from market.models import Market
from order.enums import ReserveType, OrderStatus, OrderType
from order.models import Order


class CryptoMyOrderService:
    def __init__(
        self,
        order: Order = Order,
        market: Market = Market,
    ):
        self.order = order
        self.market = market

    def get_order(self, user, _type):
        if _type == "COMPLETED":
            queryset = self.order.objects.filter(
                user=user, status=OrderStatus.COMPLETED
            ).select_related("market").order_by("-updated_at")
        elif _type == "RESERVE":
            queryset = self.order.objects.filter(
                user=user, reserve_type=ReserveType.RESERVE, status=OrderStatus.PENDING
            ).select_related("market").order_by("-updated_at")
        else:
            queryset = self.order.objects.filter(
                user=user
            ).select_related("market").order_by("-updated_at")

        return queryset
