from django.db import models


class ExchangeType(models.TextChoices):
    KRW = "KRW"
    USD = "USD"
    