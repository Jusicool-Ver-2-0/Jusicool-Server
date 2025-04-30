from django.db import models

from core.models import BaseModel
from market.enums import MarketType
from market.models import Market
from user.models import User


# Create your models here.
class Holding(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    type = models.CharField(choices=MarketType.choices)