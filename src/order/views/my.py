from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from order.serializers import OrderSerializer
from order.services.my import CryptoMyOrderService


class MyOrderView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        serializer = OrderSerializer(
            CryptoMyOrderService().get_order(
                user=request.user,
                _type=request.GET.get("type"),
            ),
            many=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
