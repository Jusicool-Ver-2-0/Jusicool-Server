import logging

from celery import shared_task
from django.db import transaction
from pykrx import stock

from market.enums import MarketType
from market.models import Market

logger = logging.getLogger(__name__)


@shared_task
@transaction.atomic
def update_stock_task():
    stock_list: list[Market] = []
    for ticker in stock.get_market_ticker_list(market="ALL"):
        stock_list.append(
            Market(
                korean_name=stock.get_market_ticker_name(ticker),
                market=ticker,
                market_type=MarketType.STOCK,
            )
        )

    Market.objects.bulk_create(
        stock_list,
        batch_size=50,
        ignore_conflicts=True
    )

    logger.info("Update Stock Batch Executed")
