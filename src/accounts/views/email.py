from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import EmailRequestSerializer, EmailValidateSerializer
from accounts.services.email import EmailService
from core.authentications import CsrfExemptSessionAuthentication


class EmailView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def get(self, request: Request) -> Response:
        serializer = EmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        EmailService().request(serializer)
        return Response(status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = EmailValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        EmailService().validate(request=request, serializer=serializer)
        return Response(status=status.HTTP_200_OK)