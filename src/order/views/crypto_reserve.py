from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from order.serializers import MarketReserveOrderSerializer
from order.services.impl.crypto_reserve import CryptoReserveOrderServiceImpl


class CryptoReserveBuyView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, crypto_id: int) -> Response:
        serializer = MarketReserveOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CryptoReserveOrderServiceImpl().reserve_buy(request.user, serializer, crypto_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CryptoReserveSellView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, crypto_id: int) -> Response:
        pass