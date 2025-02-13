import os
from celery import Celery
from django.conf import settings
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

logger.debug("Loading Celery app...")

logger.debug("Setting Django settings module...")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CryptoProject.settings")

logger.debug("Creating Celery app...")
app = Celery("CryptoProject")

logger.debug("Configuring Celery app...")
app.config_from_object("django.conf:settings", namespace="CELERY")

logger.debug("Autodiscovering tasks...")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

def debug_task(self):
    print(f"Request: {self.request!r}")

logger.debug("Celery app loaded successfully.")
