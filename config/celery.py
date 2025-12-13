from celery import Celery


app = Celery("jusicool")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.timezone = "Asia/Seoul"
