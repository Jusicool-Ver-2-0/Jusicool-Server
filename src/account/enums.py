from django.db import models


class AccountHistoryType(models.TextChoices):
    EXCHANGE = "EXCHANGE"
    ORDER = "ORDER"
