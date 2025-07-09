from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from market.serializers import MarketSerializer
from market.services.list import MarketListService


class MarketListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        serializer = MarketSerializer(
            instance=MarketListService().get_list(market_type=request.GET.get("type")),
            many=True,
        )
        return Response(serializer.data, status=200)
