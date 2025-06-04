from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from order.serializers import MyMonthOrderSerializer
from order.services.month import MonthOrderService


class MonthOrderView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request) -> Response:
        serializer = MyMonthOrderSerializer(
            MonthOrderService().get_month_orders(request.user)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)