from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from crypto.services.tick import CryptoTickService


class CryptoTickView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, crypto_code: str) -> StreamingHttpResponse:
        return StreamingHttpResponse(
            CryptoTickService().stream_crypto_tick(crypto_code),
            content_type='text/event-stream'
        )
