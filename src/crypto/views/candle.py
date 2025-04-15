from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from crypto.serializers import CryptoCandleSerializer
from crypto.services.candle import CryptoCandleService


class CryptoCandleView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, time: str) -> Response:
        candle_data = CryptoCandleService().query_candle(
            time=time,
            crypto_code=request.GET.get("crypto_code"),
            count=request.GET.get("count"),
            to=request.GET.get("to")
        )
        serializers = CryptoCandleSerializer(data=candle_data, many=True)
        serializers.is_valid(raise_exception=True)
        return Response(serializers.data, status=status.HTTP_200_OK)