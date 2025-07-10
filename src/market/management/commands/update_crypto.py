from django.core.management.base import BaseCommand
from market.tasks.crypto.update import update_crypto_task


class Command(BaseCommand):
    help = "Run update_crypto_task Celery task"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Sending update_crypto_task to Celery..."))
        result = update_crypto_task.delay()
        self.stdout.write(self.style.SUCCESS(f"Task sent. Task ID: {result.id}"))
