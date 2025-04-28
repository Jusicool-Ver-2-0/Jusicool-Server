from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    usd_balance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = ("id", "krw_balance", "usd_balance")

    def get_usd_balance(self, obj):
        return float(obj.usd_balance)