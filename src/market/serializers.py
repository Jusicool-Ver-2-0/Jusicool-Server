from rest_framework import serializers

from market.models import Market


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ("id", "korean_name", "english_name", "market", "type")

        extra_kwargs = {
            "korean_name": {"validators": []},
            "english_name": {"validators": []},
        }