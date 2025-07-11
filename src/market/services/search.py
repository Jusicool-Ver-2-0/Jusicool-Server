from django.db.models import Q
from django_redis import get_redis_connection

from market.models import Market


class MarketSearchService:
    def __init__(self, market: Market = Market):
        self.market = market
        self.redis = get_redis_connection("default")

    def search(self, query: str):
        self._save_market(query)
        return self.market.objects.filter(
            Q(korean_name__icontains=query)
            | Q(english_name__icontains=query)
            | Q(market__icontains=query)
        )

    def get_popular_market(self):
        result = self.redis.zrevrange("market::search", 0, 9, withscores=True)
        return {"keyword": [k.decode("utf-8") for k, s in result]}

    def _save_market(self, market: str):
        return self.redis.zincrby("market::search", 1, market)
