from rest_framework import serializers

from user.models import User


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()
    school = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "password", "email", "school")


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField(min_value=100000, max_value=999999)
