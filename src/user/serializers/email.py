from rest_framework import serializers


class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField(min_value=100000, max_value=999999)
