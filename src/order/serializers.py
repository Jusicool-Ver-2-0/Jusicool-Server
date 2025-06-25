from rest_framework import serializers

from order.models import Order


class MarketOrderSerializer(serializers.Serializer):
    quantity = serializers.FloatField()


class MarketReserveOrderSerializer(serializers.Serializer):
    quantity = serializers.FloatField()
    price = serializers.FloatField()


class OrderSerializer(serializers.ModelSerializer):
    market = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ("id", "market", "order_type", "reserve_type", "quantity", "price", "status")

    def get_market(self, obj):
        return obj.market.korean_name


class MyMonthOrderSerializer(serializers.Serializer):
    rate = serializers.FloatField()
    order_count = serializers.IntegerField()


class OrderPriceSerializer(serializers.Serializer):
    price = serializers.IntegerField()


class MonthlyMarketRateSerializer(serializers.Serializer):
    market = serializers.CharField()
    korean_name = serializers.CharField()
    rate = serializers.FloatField()


class MonthlyRateSerializer(serializers.Serializer):
    monthly_rate = serializers.FloatField()
    markets = MonthlyMarketRateSerializer(many=True)
