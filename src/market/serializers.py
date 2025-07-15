from rest_framework import serializers

from market.models import Market


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ("id", "korean_name", "english_name", "market", "market_type")

        extra_kwargs = {
            "korean_name": {"validators": []},
            "english_name": {"validators": []},
        }


class MarketPagedSerializer(serializers.Serializer):
    items = MarketSerializer(many=True, read_only=True)
    page = serializers.IntegerField(read_only=True)
    has_next = serializers.BooleanField(read_only=True)


class MarketPredictSerializer(serializers.Serializer):
    result = serializers.BooleanField()


class MarketPopularSearchSerializer(serializers.Serializer):
    keyword = serializers.ListSerializer(child=serializers.CharField())
