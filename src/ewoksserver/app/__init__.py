"""Start ewoks server from the command line

..code: bash

    uvicorn --factory ewoksserver.app:create_app --reload
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

try:
    from ewoksweb.serverutils import get_static_root
except ImportError:

    def get_static_root():
        return "static"


def create_app() -> FastAPI:
    app = FastAPI(
        title="ewoks",
        summary="Edit and execute ewoks workflows",
        version="1.0.0",
        contact={
            "name": "ESRF",
            "url": "https://gitlab.esrf.fr/workflow/ewoks/ewoksserver/issues",
        },
        license_info={
            "name": "MIT",
            "identifier": "MIT",
        },
    )

    _enable_cors(app)
    _mount_ewoksweb(app)

    return app


def _mount_ewoksweb(app: FastAPI) -> None:
    """Add the ewoksweb REACT application to specific paths"""
    files = StaticFiles(directory=get_static_root(), html=True)
    app.mount("/", app=files, name="ewoksweb")
    app.mount("/edit", app=files, name="ewoksweb_edit")
    app.mount("/monitor", app=files, name="ewoksweb_monitor")


def _enable_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
