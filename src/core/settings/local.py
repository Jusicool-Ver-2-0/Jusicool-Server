import os

from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "jusicool"),
        "USER": os.environ.get("DB_USER", "jusicool-postgres-admin"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "jusicool-postgres-admin-password"),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}