import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

try:
    from ewoksweb.serverutils import get_static_root
except ImportError:
    get_static_root = None


logger = logging.getLogger(__name__)


def add_frontend(app: FastAPI) -> None:
    if get_static_root is None:
        logger.info("No frontend available to serve (pip install ewoksweb)")
    else:
        files = StaticFiles(directory=get_static_root(), html=True)
        app.mount("/", app=files, name="ewoksweb")
        app.mount("/edit", app=files, name="ewoksweb_edit")
        app.mount("/monitor", app=files, name="ewoksweb_monitor")
