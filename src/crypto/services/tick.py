import httpx


class CryptoTickService:
    def __init__(self, crypto_code: str):
        self.crypto_code = crypto_code

    async def fetch_crypto_tick(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.upbit.com/v1/ticker",
                params={"markets": self.crypto_code}
            )
            response.raise_for_status()
            return response.json()