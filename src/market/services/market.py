import requests


class MarketService:
    def query_market_code(self):
        market_all_response = requests.get(
            "https://api.upbit.com/v1/market/all"
        )
        return market_all_response.json()