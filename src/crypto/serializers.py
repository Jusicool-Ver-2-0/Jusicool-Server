from rest_framework import serializers

from market.models import Market


class CryptoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ("id", "korean_name", "english_name")
