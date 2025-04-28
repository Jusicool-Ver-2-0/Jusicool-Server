from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import AccountSerializer
from account.services.my import MyAccountService
from core.authentications import CsrfExemptSessionAuthentication


class MyAccountView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request) -> Response:
        serializer = AccountSerializer(
            instance=MyAccountService().get_my_account(request.user)
        )
        return Response(serializer.data, status=status.HTTP_200_OK)