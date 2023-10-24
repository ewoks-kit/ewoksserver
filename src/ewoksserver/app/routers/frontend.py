import logging
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

try:
    from ewoksweb.serverutils import get_static_root
except ImportError:
    get_static_root = None

router = APIRouter()

logger = logging.getLogger(__name__)  # TODO: root logger level from CLI


if get_static_root is None:
    logger.info("No frontend available to serve (pip install ewoksweb)")
else:
    files = StaticFiles(directory=get_static_root(), html=True)
    router.mount("/", app=files, name="ewoksweb")
    router.mount("/edit", app=files, name="ewoksweb_edit")
    router.mount("/monitor", app=files, name="ewoksweb_monitor")
