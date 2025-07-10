from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from exchange.enums import ExchangeType
from exchange.serializers import ExchangeSerializer
from exchange.services.exchange import ExchangeService


class ExchangeView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, exchange_type: ExchangeType) -> Response:
        serializer = ExchangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ExchangeService().exchange(
            user=request.user, serializer=serializer, exchange_type=exchange_type
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
