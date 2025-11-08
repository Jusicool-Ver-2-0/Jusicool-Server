from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers.signup import SignupSerializer
from user.services.user import UserService
from core.authentications import CsrfExemptSessionAuthentication


class SignupView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request: Request) -> Response:
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserService().signup(serializer)
        return Response(status=status.HTTP_201_CREATED)
