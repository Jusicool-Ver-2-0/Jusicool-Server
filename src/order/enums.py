from django.db import models


class OrderType(models.TextChoices):
    BUY = "BUY"
    SELL = "SELL"


class ReserveType(models.TextChoices):
    RESERVE = "RESERVE"
    NOW = "NOW"


class OrderStatus(models.TextChoices):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"