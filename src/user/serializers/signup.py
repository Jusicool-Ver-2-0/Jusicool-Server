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
