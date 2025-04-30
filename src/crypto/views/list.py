from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from crypto.serializers import CryptoListSerializer
from crypto.services.list import CryptoListService


class CryptoListView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request) -> Response:
        crypto_list = CryptoListService().get_crypto_list()
        serializer = CryptoListSerializer(crypto_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)