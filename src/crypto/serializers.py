from rest_framework import serializers


class CryptoSerializer(serializers.Serializer):
    market = serializers.CharField()
    korean_name = serializers.CharField()
    english_name = serializers.CharField()


class CryptoCandleSerializer(serializers.Serializer):
    market = serializers.CharField()
    candle_date_time_utc = serializers.DateTimeField()
    candle_date_time_kst = serializers.DateTimeField()
    opening_price = serializers.FloatField()
    high_price = serializers.FloatField()
    low_price = serializers.FloatField()
    trade_price = serializers.FloatField()
    timestamp = serializers.IntegerField()
    candle_acc_trade_price = serializers.FloatField()
    candle_acc_trade_volume = serializers.FloatField()