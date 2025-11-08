from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class User(BaseModel, AbstractUser):

    email = models.EmailField(unique=True)
    school = models.CharField(max_length=255, null=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "user"
