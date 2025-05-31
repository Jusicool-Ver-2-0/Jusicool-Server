from django.core.cache import cache

from market.models import Market


class MarketListService:
    def __init__(self, market: Market = Market):
        self.market = market

    def get_list(self, market_type: str = None):
        return cache.get_or_set(
            f"market::list::{market_type or 'ALL'}",
            lambda: self._fetch_from_db(market_type),
            timeout=60 * 60 * 24
        )

    def _fetch_from_db(self, market_type: str = None):
        if market_type:
            return self.market.objects.filter(market_type=market_type)
        return self.market.objects.all()