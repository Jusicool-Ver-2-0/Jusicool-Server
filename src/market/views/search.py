from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from market.serializers import MarketSerializer
from market.services.search import MarketSearchService


class MarketSearchView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    market_search_service = MarketSearchService()

    def get(self, request: Request) -> Response:
        serializer = MarketSerializer(
            self.market_search_service.search(request.GET.get('query')),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)