from abc import abstractmethod, ABC


class ReserveOrderService(ABC):
    @abstractmethod
    def reserve_buy(self, user, serializer, market_id: int):
        raise NotImplementedError

    @abstractmethod
    def reserve_sell(self, user, serializer, market_id: int):
        raise NotImplementedError

    @abstractmethod
    def _fetch_trade_price(self, market: str) -> float:
        raise NotImplementedError

    def _calculate_price(self, market: str, quantity: float) -> (float, float):
        crypto_trade_price = self._fetch_trade_price(market)
        return crypto_trade_price, crypto_trade_price * quantity