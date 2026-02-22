from celery import Celery

from src.share.core.config import settings
from src.worker.constants import TICKER_PRICE_TASK_NAME


CRON_TIME = 60


celery_app = Celery(
    'celery_app',
    broker=settings.redis_celery_broker_url,
    backend=settings.redis_celery_broker_url,
    include=['src.worker.tasks', 'src.worker.lifespan']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    'add_ticker-prices': {
        'task': TICKER_PRICE_TASK_NAME,
        'schedule': CRON_TIME,
    },
}
