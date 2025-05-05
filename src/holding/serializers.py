from rest_framework import serializers

from holding.models import Holding
from market.serializers import MarketSerializer


class HoldingSerializer(serializers.ModelSerializer):
    market = MarketSerializer()

    class Meta:
        model = Holding
        fields = ("id", "market", "quantity", "price")
