from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel
from user.enums import UserStatus


class User(BaseModel, AbstractUser):

    email = models.EmailField(unique=True)
    school = models.CharField(max_length=255, null=True)

    status = models.CharField(
        max_length=8,
        choices=UserStatus.choices,
        default=UserStatus.PENDING,
        null=True
    )

    class Meta:
        db_table = "user"
