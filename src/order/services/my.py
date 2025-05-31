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

    def get(self, user, order_type, order_status, market, reserve_type):
        return self.order.objects.filter(
            user=user,
            reserve_type=ReserveType(reserve_type),
            market__market_type=MarketType(market),
            order_type=OrderType(order_type),
            status=OrderStatus(order_status),
        )
