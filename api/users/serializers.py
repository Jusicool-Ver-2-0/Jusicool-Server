from rest_framework import serializers


class SendVerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="이메일 주소",
    )
