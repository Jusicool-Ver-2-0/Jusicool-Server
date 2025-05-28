from market.enums import MarketType
from market.models import Market


class CryptoListService:
    def __init__(self, market: Market = Market):
        self.market = market

    def get_crypto_list(self):
        return self.market.objects.filter(market_type=MarketType.CRYPTO.value)
