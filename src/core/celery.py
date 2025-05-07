from celery import Celery
from celery.schedules import crontab


app = Celery("jusicool")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = "Asia/Seoul"


app.conf.beat_schedule = {
    "update_crypto": {
        "task": "market.tasks.update_crypto",
        "schedule": crontab(hour=0, minute=0),
    }
}
