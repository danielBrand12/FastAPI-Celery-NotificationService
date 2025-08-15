from celery import Celery
import os
from app.core.settings import settings

CELERY_BROKER = settings.CELERY_BROKER_URL

celery_config = {
    "broker_url": CELERY_BROKER,
    "result_expires": 7200,
    "worker_prefetch_multiplier": 1,
    "task_track_started": True,
    "task_serializer": "pickle",
    "accept_content": ["pickle", "json"],
}


celery_app = Celery("worker", config_source=celery_config)