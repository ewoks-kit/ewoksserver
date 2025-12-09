"""Start ewoks server from the command line with the Uvicorn CLI

.. code-block:: bash

    uvicorn ewoksserver.main:app

or the FastAPI CLI

.. code-block:: bash

    fastapi dev src/ewoksserver/main.py

.. code-block:: bash

    fastapi run src/ewoksserver/main.py
"""

from .app import create_app
from .config import configure_app

_ = configure_app()
app = create_app()
