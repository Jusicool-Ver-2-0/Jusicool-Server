from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

# 테스트에서 이메일 전송 방지
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
