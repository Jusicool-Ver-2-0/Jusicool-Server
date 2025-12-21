from rest_framework import serializers


class SendVerifyCodeSerializer(serializers.Serializer):
    """이메일 인증 요청"""

    email = serializers.EmailField(
        help_text="이메일 주소",
    )
