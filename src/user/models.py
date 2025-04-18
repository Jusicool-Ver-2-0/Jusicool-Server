from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class User(BaseModel, AbstractUser):
    class UserStatus(models.TextChoices):
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"
        PENDING = "PENDING"

    email = models.EmailField(unique=True)
    school = models.CharField(max_length=255)

    status = models.CharField(
        max_length=8,
        choices=UserStatus,
        default=UserStatus.PENDING
    )

    class Meta:
        db_table = "user"
