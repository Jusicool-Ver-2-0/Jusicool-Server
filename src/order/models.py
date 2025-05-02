from django.db import models

from core.models import BaseModel
from order.enums import ReserveType, OrderType, OrderStatus
from user.models import User


# Create your models here.
class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_type = models.CharField(
        choices=OrderType.choices,
        max_length=4
    )
    reserve_type = models.CharField(
        choices=ReserveType.choices,
        max_length=7
    )
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        choices=OrderStatus.choices,
        max_length=9
    )
    price = models.PositiveBigIntegerField()

    class Meta:
        db_table = 'order'