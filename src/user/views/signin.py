from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import SigninSerializer
from user.services.account import AccountService
from core.authentications import CsrfExemptSessionAuthentication


class SigninView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def post(self, request: Request) -> Response:
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AccountService().signin(request=request, serializer=serializer)
        return Response(status=status.HTTP_200_OK)