import os
from celery import Celery

# Set the default Django settings module for  the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto.settings')

# Create an instance of the app
app = Celery('crypto')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto discovers asynchronous tasks in each app
app.autodiscover_tasks()