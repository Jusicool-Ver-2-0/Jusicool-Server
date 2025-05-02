from abc import ABC, abstractmethod


class OrderService(ABC):
    @abstractmethod
    def buy(self, user, serializer, market_id: int):
        raise NotImplementedError

    @abstractmethod
    def sell(self, user, serializer, market_id: int):
        raise NotImplementedError

    @abstractmethod
    def _fetch_trade_price(self, market: str) -> float:
        raise NotImplementedError

    def _calculate_price(self, market: str, quantity: float) -> (float, float):
        crypto_trade_price = self._fetch_trade_price(market)
        return crypto_trade_price, crypto_trade_price * quantity