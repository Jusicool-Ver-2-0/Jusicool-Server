from market.models import Market


class MarketListService:
    def __init__(self, market: Market = Market):
        self.market = market

    def get_list(self, market_type: str = None):
        if market_type:
            return self.market.objects.filter(market_type=market_type)
        return self.market.objects.all()