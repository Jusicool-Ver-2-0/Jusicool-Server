from rest_framework import serializers


class MarketOrderSerializer(serializers.Serializer):
    quantity = serializers.FloatField()


class MarketReserveOrderSerializer(serializers.Serializer):
    quantity = serializers.FloatField()
    price = serializers.FloatField()