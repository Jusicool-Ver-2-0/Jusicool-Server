from django.core.management.base import BaseCommand
from market.tasks.stock.update import update_stock_task

class Command(BaseCommand):
    help = 'Run update_stock_task Celery task'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Sending update_stock_task to Celery..."))
        result = update_stock_task.delay()
        self.stdout.write(self.style.SUCCESS(f"Task sent. Task ID: {result.id}"))
