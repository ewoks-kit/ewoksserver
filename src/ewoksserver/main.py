"""Start ewoks server from the command line

..code: bash

    uvicorn ewoksserver.main:app --reload
"""

from .app import create_app

app = create_app()
