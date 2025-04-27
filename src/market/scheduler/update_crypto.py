import requests
from apscheduler.schedulers.background import BackgroundScheduler

from django.conf import settings
from django.db import transaction

from market.enums import MarketType
from market.models import Market
from market.serializers import MarketSerializer


@transaction.atomic
def update_crypto():
    crypto_market_response = requests.get(
        settings.CRYPTO_API_BASE_URL + "/market/all",
    )

    serializer = MarketSerializer(
        data=[
            {
                "type": MarketType.CRYPTO.value,
                "korean_name": c["korean_name"],
                "english_name": c["english_name"],
            } for c in crypto_market_response.json()
        ],
        many=True
    )
    serializer.is_valid(raise_exception=True)

    Market.objects.bulk_create(
        [
            Market(**s)
            for s in serializer.data
        ],
        ignore_conflicts=True
    )

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_crypto, "cron", hour=0, minute=0)
    scheduler.start()