from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import EmailRequestSerializer, EmailValidateSerializer
from user.services.email import EmailService
from core.authentications import CsrfExemptSessionAuthentication


class EmailRequestView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def post(self, request: Request) -> Response:
        serializer = EmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        EmailService().request(serializer)
        return Response(status=status.HTTP_200_OK)


class EmailValidateView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, )

    def post(self, request: Request) -> Response:
        serializer = EmailValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        EmailService().validate(request=request, serializer=serializer)
        return Response(status=status.HTTP_200_OK)


