from django.db import models

from account.enums import AccountHistoryType
from core.models import BaseModel
from user.models import User


# Create your models here.
class Account(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    krw_balance = models.PositiveIntegerField(default=0)
    usd_balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    class Meta:
        db_table = "account"


class AccountHistory(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    changed_krw = models.BigIntegerField(default=0)
    changed_usd = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    history_type = models.CharField(
        choices=AccountHistoryType.choices,
        max_length=8,
    )

    class Meta:
        db_table = "account_history"