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
            )
        elif _type == "RESERVE":
            queryset = self.order.objects.filter(
                user=user, reserve_type=ReserveType.RESERVE, status=OrderStatus.PENDING
            )
        else:
            queryset = self.order.objects.filter(user=user)

        return queryset
