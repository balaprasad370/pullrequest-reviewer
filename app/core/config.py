import os
from celery import Celery
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")  # ✅ use service name

redis_client = redis.Redis.from_url(REDIS_URL)

celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

from app.tasks import analyze_pr
