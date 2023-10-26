"""Start ewoks server from the command line

..code: bash

    uvicorn --factory ewoksserver.app:create_app --reload
"""

import logging
from pprint import pformat
from fastapi import FastAPI

from .cors import enable_cors
from .lifespan import fastapi_lifespan
from .routes import versioning
from .routes import frontend
from .routes import tasks
from .routes import workflows
from .routes import icons
from .routes import execution

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create the main API instance"""
    versioning.assert_route_versions(
        tasks.routers,
        workflows.routers,
        icons.routers,
        execution.routers,
        execution.app_creators,
    )
    all_parsed_routes = (
        versioning.parse_routes("tasks", tasks.routers),
        versioning.parse_routes("workflows", workflows.routers),
        versioning.parse_routes("icons", icons.routers),
        versioning.parse_routes("execution", execution.routers),
        versioning.parse_routes(
            "execution", execution.app_creators, prefix="socket.io"
        ),
    )
    version_tags = versioning.extract_version_tags(all_parsed_routes)
    major, minor, patch = versioning.extract_lastest_version(all_parsed_routes)

    tags_metadata = [
        {"name": "tasks", "description": "Ewoks workflow tasks"},
        {"name": "workflows", "description": "Ewoks workflows"},
        {"name": "icons", "description": "Ewoks workflow icons"},
        {"name": "execution", "description": "Ewoks workflow execution"},
        *(
            {"name": tag, "description": f"Ewoks workflows API {tag}"}
            for tag in version_tags
        ),
    ]

    app = FastAPI(
        title="ewoks",
        summary="Edit and execute ewoks workflows",
        version=f"{major}.{minor}.{patch}",
        contact={
            "name": "ESRF",
            "url": "https://gitlab.esrf.fr/workflow/ewoks/ewoksserver/issues",
        },
        license_info={
            "name": "MIT",
            "identifier": "MIT",
        },
        openapi_tags=tags_metadata,
        lifespan=fastapi_lifespan,
    )

    enable_cors(app)

    versioning.add_routes(app, all_parsed_routes, skip_older_versions=True)

    frontend.add_frontend(app)  # Needs to come last for some reason

    logger.info(f"Routes \n {pformat(app.routes)}")

    return app
