import requests


class CryptoService:
    def query_crypto_code(self):
        crypto_all_response = requests.get(
            "https://api.upbit.com/v1/market/all"
        )
        return crypto_all_response.json()