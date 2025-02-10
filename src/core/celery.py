from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

celery_app = Celery("crypto_blocks")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks()


celery_app.conf.beat_schedule.update(
    {
        "fetch-latest-blocks": {
            "task": "apps.blocks.tasks.fetch_latest_blocks",
            "schedule": crontab(minute="*/2"),
        }
    }
)
