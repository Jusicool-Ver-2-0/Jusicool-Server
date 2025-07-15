from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from market.services.list import MarketListService


class MarketListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        return Response(
            MarketListService().get_list(
                market_type=request.GET.get("type"),
                size=request.GET.get("size"),
                page=request.GET.get("page"),
            ),
            status=status.HTTP_200_OK,
        )
