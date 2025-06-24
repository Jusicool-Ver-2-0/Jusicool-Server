from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from order.services.monthly import MonthlyService


class MonthlyView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    monthly_service = MonthlyService()

    def get(self, request: Request) -> Response:
        return Response(
            data=self.monthly_service.get_monthly_percent(user=request.user).data,
            status=status.HTTP_200_OK,
        )