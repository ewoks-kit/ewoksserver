from pathlib import Path

RESOURCE_DIRECTORY = str(Path(__file__).resolve().parent)

EWOKS = {
    "handlers": [
        {
            "class": "ewokscore.events.handlers.Sqlite3EwoksEventHandler",
            "arguments": [
                {
                    "name": "uri",
                    "value": "file:ewoks_events.db",
                }
            ],
        }
    ]
}

# CELERY = {
#    "broker_url": "redis://localhost:25001/2",
#    "result_backend": "redis://localhost:25001/3",
# }


EWOKS_DISCOVERY = {
    "on_start_up": True,
    "timeout": 60,
}
