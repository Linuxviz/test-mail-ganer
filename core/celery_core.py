import os

from celery import Celery
# Django settings place
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
# CELERY prefix for const names in settings file
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()