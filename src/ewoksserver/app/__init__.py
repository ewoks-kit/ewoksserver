"""Start ewoks server from the command line

..code: bash

    uvicorn --factory ewoksserver.app:create_app --reload
"""


from fastapi import FastAPI

from .cors import enable_cors
from .lifespan import fastapi_lifespan
from .routers import utils as router_utils
from .routers import tasks
from .routers import workflows
from .routers import icons
from .routers import frontend


def create_app() -> FastAPI:
    """Create the main API instance"""
    all_parsed_routers = (
        router_utils.parse_routers("tasks", tasks.routers),
        router_utils.parse_routers("workflows", workflows.routers),
        router_utils.parse_routers("icons", icons.routers),
    )
    major, minor, patch = router_utils.extract_version(all_parsed_routers)

    tags_metadata = [
        {"name": "tasks", "description": "Ewoks workflow tasks"},
        {"name": "workflows", "description": "Ewoks workflows"},
        {"name": "icons", "description": "Ewoks workflow icons"},
        *(
            {"name": name, "description": f"Ewoks workflows API {name}"}
            for name in router_utils.extract_version_tags(all_parsed_routers)
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
        routers=[frontend.router],
    )

    enable_cors(app)
    router_utils.add_routes(app, all_parsed_routers)
    return app
