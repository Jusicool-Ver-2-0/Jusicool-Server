from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.users.schema import email_send_schema
from api.users.serializers import SendVerifyCodeSerializer
from apps.users.services import UserVerificationService
from core.exceptions import InvalidRequestError
from core.throttles import TwoRequestPerOneMinuteAnonRateThrottle


class EmailRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [TwoRequestPerOneMinuteAnonRateThrottle]

    @email_send_schema
    def post(self, request: Request) -> Response:
        input_serializer = SendVerifyCodeSerializer(data=request.data)
        if not input_serializer.is_valid():
            raise InvalidRequestError

        UserVerificationService().send_verification_code(
            email=input_serializer.validated_data["email"],
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
