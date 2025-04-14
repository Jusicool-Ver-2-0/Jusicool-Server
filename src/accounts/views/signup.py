from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import SignupSerializer
from accounts.services.account import AccountService
from core.authentications import CsrfExemptSessionAuthentication


class SignupView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def post(self, request: Request) -> Response:
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        AccountService().signup(serializer)
        return Response(status=status.HTTP_201_CREATED)