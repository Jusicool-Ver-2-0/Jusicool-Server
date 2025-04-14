from rest_framework import serializers


class MarketSerializer(serializers.Serializer):
    market = serializers.CharField()
    korean_name = serializers.CharField()
    english_name = serializers.CharField()