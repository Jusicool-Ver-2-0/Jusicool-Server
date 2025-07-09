import requests
from django.conf import settings
from django.core.cache import cache

from market.serializers import MarketPredictSerializer


class MarketPredictService:
    def predict(self, market_code: str):
        result = cache.get_or_set(
            f"market::predict::{market_code}",
            lambda: self._fetch_market_predict_service(market_code),
            timeout=60 * 60 * 3
        )
        return MarketPredictSerializer({"result": result}).data

    @staticmethod
    def _fetch_market_predict_service(market_code: str) -> bool:
        response = requests.post(
            f"{settings.PREDICT_API_BASE_URL}/predict",
            json={"market": market_code}
        )
        if not response.status_code == 200:
            raise Exception(f"Failed to fetch prediction for market {market_code}. "
                            f"Status code: {response.status_code}, Response: {response.text}")

        return response.json().get("result")