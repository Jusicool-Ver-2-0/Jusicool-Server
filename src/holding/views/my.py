from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from holding.serializers import HoldingSerializer
from holding.services.my import MyHoldingService


class MyHoldingView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request) -> Response:
        my_holding = MyHoldingService().get_my_holding(request.user)
        serializer = HoldingSerializer(instance=my_holding, many=True)
        return Response(serializer.data)