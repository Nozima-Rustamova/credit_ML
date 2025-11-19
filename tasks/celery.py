# tasks/celery.py
import os
from celery import Celery
from celery.schedules import crontab

# set default Django settings module for 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "credit_risk.settings")

app = Celery("credit_risk")

# Read configuration from Django settings, CELERY_ prefixed keys are supported.
app.config_from_object("django.conf:settings", namespace="CELERY")

# You can list modules to autodiscover tasks from. We'll import tasks explicitly below,
# but keep autodiscover for tasks defined as app.task in installed apps.
app.autodiscover_tasks()

# Periodic schedule example (runs beat jobs):
app.conf.beat_schedule = {
    # cleanup logs monthly
    "cleanup-prediction-logs-monthly": {
        "task": "tasks.tasks.cleanup_prediction_logs",
        "schedule": crontab(day_of_month=1, hour=4, minute=0),
        "args": (90,),  # delete logs older than 90 days
    },
    # rescore pending credit requests every hour
    "rescore-pending-credit-requests": {
        "task": "tasks.tasks.rescore_pending_credit_requests",
        "schedule": crontab(minute="*/30"),  # every 30 minutes
        "args": (100,),  # process up to 100 pending requests per run
    },
    # refresh stale external records daily
    "refresh-stale-external-records": {
        "task": "tasks.tasks.refresh_stale_external_records",
        "schedule": crontab(hour=3, minute=30),
        "args": (30,),  # TTL days
    },
}

# Optional: make sure tasks module is imported so tasks register
# (this import is safe even if file doesn't exist yet)
try:
    import tasks.tasks  # noqa: F401
except Exception:
    # don't explode at import time if tasks module errors; Celery worker logs will show issues
    pass