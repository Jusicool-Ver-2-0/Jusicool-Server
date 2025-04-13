from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class Account(BaseModel, AbstractUser):
    class AccountStatus(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"
        PENDING = "PENDING"

    email = models.EmailField(unique=True)
    school = models.CharField(max_length=255)

    status = models.CharField(
        max_length=8,
        choices=AccountStatus,
        default=AccountStatus.PENDING
    )

    class Meta:
        db_table = "account"
