# tasks/__init__.py
# Expose Celery app for 'celery -A tasks worker' style invocations.
from .celery import app as celery_app

__all__ = ("celery_app",)