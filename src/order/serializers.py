from rest_framework import serializers

from order.models import Order


class MarketOrderSerializer(serializers.Serializer):
    quantity = serializers.FloatField()


class MarketReserveOrderSerializer(serializers.Serializer):
    quantity = serializers.FloatField()
    price = serializers.FloatField()


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "market", "order_type", "reserve_type", "quantity", "price", "status")
