import asyncio
from typing import AsyncGenerator

from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from core.sse import SseFormatter
from crypto.serializers import CryptoTickSerializer
from crypto.services.tick import CryptoTickService


class CryptoTickView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, crypto_code: str) -> StreamingHttpResponse:
        return StreamingHttpResponse(
            self._stream_crypto_data(crypto_code),
            content_type='text/event-stream'
        )

    async def _stream_crypto_data(self, crypto_code: str) -> AsyncGenerator[str]:
        service = CryptoTickService(crypto_code)
        while True:
            data = await service.fetch_crypto_tick()

            serializer = CryptoTickSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)

            yield SseFormatter.to_sse(serializer.data)

            await asyncio.sleep(0.5)