from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from market.services.predict import MarketPredictService


class MarketPredictView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    market_predict_service = MarketPredictService()

    def get(self, request: Request, market_code: str) -> Response:
        return Response(
            self.market_predict_service.predict(market_code), status=status.HTTP_200_OK
        )
