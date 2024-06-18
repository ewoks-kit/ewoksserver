import os
from ewoksserver.app.config import EwoksSettingsType


def has_celery(settings: EwoksSettingsType) -> bool:
    if os.getenv("BEACON_HOST"):
        return True

    return bool(settings.celery)
