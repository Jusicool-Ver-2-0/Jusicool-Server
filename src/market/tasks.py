import logging

import requests
from celery import shared_task
from django.conf import settings

from market.enums import MarketType
from market.models import Market
from market.serializers import MarketSerializer

logger = logging.getLogger(__name__)


@shared_task
def update_crypto():
    crypto_market_response = requests.get(
        settings.CRYPTO_API_BASE_URL + "/market/all",
    )
    if crypto_market_response.status_code != 200:
        logger.error(
            f"Crypto API request failed: "
            f"{crypto_market_response.status_code}, "
            f"{crypto_market_response.text}"
        )
        raise Exception("Crypto API request failed")

    serializer = MarketSerializer(
        data=[
            {
                "type": MarketType.CRYPTO.value,
                "korean_name": c["korean_name"],
                "english_name": c["english_name"],
                "market": c["market"]
            } for c in crypto_market_response.json() if c["market"].startswith("KRW")
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
    logger.error("Update Crypto Batch Executed")