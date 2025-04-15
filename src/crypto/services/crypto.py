import requests
from django.core.cache import cache


class CryptoService:
    def query_crypto_code(self):
        return cache.get_or_set(
            key="crypto:code",
            default=lambda: self._fetch_crypto_code(),
            timeout=60 * 60 * 10
        )

    def _fetch_crypto_code(self):
        crypto_all_response = requests.get(
            "https://api.upbit.com/v1/market/all"
        )
        return crypto_all_response.json()