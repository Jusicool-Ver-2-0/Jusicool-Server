from django.core.exceptions import ValidationError
from django.db import models

from account.enums import AccountHistoryType
from core.models import BaseModel
from order.models import Order
from user.models import User


# Create your models here.
class Account(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    krw_balance = models.PositiveBigIntegerField(default=0)
    usd_balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)

    class Meta:
        db_table = "account"


class AccountHistory(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    changed_krw = models.BigIntegerField(default=0)
    changed_usd = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    history_type = models.CharField(
        choices=AccountHistoryType.choices,
        max_length=8,
    )

    class Meta:
        db_table = "account_history"

    def clean(self):
        # Type이 Order이지만 order이 Null일때
        if (self.history_type == AccountHistoryType.ORDER.value) and (
            self.order is None
        ):
            raise ValidationError({"error": "AccountHistoryType.ORDER must be set"})
