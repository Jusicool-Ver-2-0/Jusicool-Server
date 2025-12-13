"""
Django가 시작될 때 Celery app을 로드합니다.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
