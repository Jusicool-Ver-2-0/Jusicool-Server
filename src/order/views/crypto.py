from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from order.serializers import MarketOrderSerializer
from order.services.impl.crypto import CryptoOrderServiceImpl


class CryptoBuyView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request: Request, crypto_id: int) -> Response:
        serializer = MarketOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CryptoOrderServiceImpl().buy(user=request.user, serializer=serializer, market_id=crypto_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CryptoSellView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def post(self, request: Request, crypto_id: int) -> Response:
        serializer = MarketOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CryptoOrderServiceImpl().sell(user=request.user, serializer=serializer, market_id=crypto_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
