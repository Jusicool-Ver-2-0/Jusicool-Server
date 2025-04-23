import requests
from django.core.cache import cache


class CryptoCandleService:
    def query_candle(self, time, crypto_code, count, to):
        return cache.get_or_set(
            key=f"crypto:candle:{time}:{crypto_code}:{count}:{to}",
            default=lambda: self._fetch_candle(time, crypto_code, count, to),
            timeout=60 * 60 * 3
        )

    def _fetch_candle(self, time, crypto_code, count, to):
        candle_query_response = requests.get(
            f"https://api.upbit.com/v1/candles/{time}",
            params={
                "market": crypto_code,
                'count': count,
                "to": to
            }
        )
        return candle_query_response.json()
