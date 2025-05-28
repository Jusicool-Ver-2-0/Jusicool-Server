from abc import ABC, abstractmethod

import requests
from django.conf import settings

from core.kis import kis
from market.enums import MarketType
from order.exceptions import TradePriceFetchException


class OrderService(ABC):
    @abstractmethod
    def buy(self):
        raise NotImplementedError

    @abstractmethod
    def sell(self):
        raise NotImplementedError

    def _calculate_price(self, market: str, quantity: float, market_type: str) -> (float, float):
        crypto_trade_price = float
        if market_type == MarketType.CRYPTO:
            crypto_trade_price = self._fetch_crypto_trade_price(market)
        elif market_type == MarketType.STOCK:
            crypto_trade_price = self._fetch_stock_trade_price(market)
        return crypto_trade_price, crypto_trade_price * quantity

    def _fetch_crypto_trade_price(self, market: str) -> float:
        crypto_trade_price = requests.get(
            f"{settings.CRYPTO_API_BASE_URL}/ticker",
            params={"markets": market},
        )
        if crypto_trade_price.status_code != 200:
            raise TradePriceFetchException()
        return float(crypto_trade_price.json()[0].get("trade_price"))

    def _fetch_stock_trade_price(self, market: str) -> int:
        return kis.get_kr_current_price(market)