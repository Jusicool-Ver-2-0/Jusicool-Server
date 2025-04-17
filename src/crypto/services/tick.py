import asyncio

import aiohttp


class CryptoTickService:
    async def stream_crypto_tick(self, crypto_code):
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(
                    "https://api.upbit.com/v1/ticker",
                    params={"markets": crypto_code},
                ) as response:
                    yield f"data: {await response.json()}\n\n"
                    await asyncio.sleep(1)