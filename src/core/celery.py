from datetime import timedelta

from celery import Celery
from celery.schedules import crontab


app = Celery("jusicool")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = "Asia/Seoul"


app.conf.beat_schedule = {
    "update_crypto_task": {
        "task": "market.tasks.crypto.update.update_crypto_task",
        "schedule": crontab(hour=0, minute=0),
    },
    "update_stock_task": {
        "task": "market.tasks.stock.update.update_stock_task",
        "schedule": crontab(hour=0, minute=0),
    },
    "crypto_reserve_buy_task": {
        "task": "order.tasks.crypto.buy.crypto_reserve_buy_task",
        "schedule": timedelta(seconds=1),
    },
    "crypto_reserve_sell_task": {
        "task": "order.tasks.crypto.sell.crypto_reserve_sell_task",
        "schedule": timedelta(seconds=1),
    }
}
