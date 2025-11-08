from rest_framework import serializers


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
