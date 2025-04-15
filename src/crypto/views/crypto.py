from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.authentications import CsrfExemptSessionAuthentication
from src.crypto.serializers import CryptoSerializer
from src.crypto.services.crypto import CryptoService


class CryptoView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request) -> Response:
        crypto_data = CryptoService().query_crypto_code()
        serializer = CryptoSerializer(data=crypto_data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)