from rest_framework import serializers

from accounts.models import Account


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()
    school = serializers.CharField()

    class Meta:
        model = Account
        fields = ("username", "password", "email", "school")


class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField(
        min_value=100000,
        max_value=999999
    )