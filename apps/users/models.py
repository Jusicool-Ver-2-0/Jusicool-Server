from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    email = models.EmailField(
        "사용자 이메일 주소",
        unique=True,
    )

    school = models.CharField(
        "학교 코드",
        null=True,
    )

    class Meta:
        db_table = "user"
