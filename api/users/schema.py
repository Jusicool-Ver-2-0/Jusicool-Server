from drf_spectacular.utils import OpenApiExample, extend_schema

from api.users.serializers import SendVerifyCodeSerializer

email_send_schema = extend_schema(
    tags=["users"],
    summary="Send email verification code",
    description="사용자 이메일로 인증 코드를 발송합니다. 분당 최대 2회의 요청만 허용됩니다.",
    request=SendVerifyCodeSerializer,
    responses={204: None},
    examples=[
        OpenApiExample(
            name="Valid request",
            value={"email": "user@example.com"},
            request_only=True,
        )
    ],
)
