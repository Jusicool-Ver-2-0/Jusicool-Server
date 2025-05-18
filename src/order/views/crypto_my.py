from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from order.serializers import OrderSerializer
from order.services.crypto_my import CryptoMyOrderService


class CryptoMyOrderView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        order_type = request.GET.get("type")
        order_data = CryptoMyOrderService().get(request.user, order_type)
        serializer = OrderSerializer(order_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)