from rest_framework import serializers


class ExchangeSerializer(serializers.Serializer):
    amount = serializers.FloatField()
