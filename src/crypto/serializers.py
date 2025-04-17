from rest_framework import serializers


class CryptoSerializer(serializers.Serializer):
    market = serializers.CharField()
    korean_name = serializers.CharField()
    english_name = serializers.CharField()


class CryptoCandleSerializer(serializers.Serializer):
    market = serializers.CharField()

    opening_price = serializers.FloatField()  # 시가
    high_price = serializers.FloatField()  # 고가
    low_price = serializers.FloatField()  # 저가
    trade_price = serializers.FloatField()  # 종가

    candle_acc_trade_price = serializers.FloatField()  # 누적 거래 대금
    candle_acc_trade_volume = serializers.FloatField()  # 누적 거래량

    candle_date_time_utc = serializers.DateTimeField()
    candle_date_time_kst = serializers.DateTimeField()
    timestamp = serializers.IntegerField()


class CryptoTickSerializer(serializers.Serializer):
    market = serializers.CharField()

    opening_price = serializers.FloatField()  # 시가
    high_price = serializers.FloatField()  # 고가
    low_price = serializers.FloatField()  # 저가
    trade_price = serializers.FloatField()  # 종가

    acc_trade_price = serializers.FloatField()  # 누적 거래 대금
    acc_trade_price_24h = serializers.FloatField()  # 24시간 누적 거래 대금
    acc_trade_volume = serializers.FloatField()  # 누적 거래량
    acc_trade_volume_24h = serializers.FloatField()  # 24시간 누적 거래량

    timestamp = serializers.IntegerField()