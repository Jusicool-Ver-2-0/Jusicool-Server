from django.db import models

from user.models import User
from core.models import BaseModel


# Create your models here.
class CryptoTrade(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_code = models.CharField()
    trade_price = models.FloatField()