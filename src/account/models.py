from django.db import models

from core.models import BaseModel
from user.models import User


# Create your models here.
class Account(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    krw_balance = models.PositiveBigIntegerField()
    usd_balance = models.DecimalField(max_digits=20, decimal_places=2)


class AccountTransaction(BaseModel):
    class AccountTransactionType(models.TextChoices):
        EXCHANGE = "EXCHANGE"

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=AccountTransactionType)
    changed_krw_balance = models.BigIntegerField()
    changed_usd_balance = models.DecimalField(max_digits=20, decimal_places=2)
