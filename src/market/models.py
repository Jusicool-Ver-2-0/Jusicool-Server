from django.db import models

from core.models import BaseModel
from market.enums import MarketType


class Market(BaseModel):
    korean_name = models.CharField(max_length=255, unique=True)
    english_name = models.CharField(max_length=255, unique=True)
    market = models.CharField(max_length=255)
    type = models.CharField(
        choices=MarketType.choices,
        max_length=6
    )

    class Meta:
        db_table = "market"