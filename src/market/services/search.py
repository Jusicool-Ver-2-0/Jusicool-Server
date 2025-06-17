from django.db.models import Q

from market.models import Market


class MarketSearchService:
    def __init__(self, market: Market = Market):
        self.market = market

    def search(self, query: str):
        return self.market.objects.filter(
            Q(korean_name__icontains=query) |
            Q(english_name__icontains=query) |
            Q(market__icontains=query)
        )