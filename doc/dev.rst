Developers information
======================

Starting the server
-------------------

To allow for custom command line arguments, an entry point is created to start the server

.. code:: python

    ewoks-server

If none of the ewoks specific parameters like `--rediscover-tasks` need to be specified you
can also do this

.. code:: python

    uvicorn --factory ewoksserver.app:create_app

Most FastAPI projects provide a module with a global FastAPI instance to allow starting the
server like this

.. code:: python

    uvicorn <projectname>.main:app

Ewoksserver does not provide this.

API versioning
--------------

By default the server provides versioned end-points for all full and major versions. For example

.. code::

    GET /api/workflows          # same as v2_0_0

    GET /api/v2/workflows       # same as v2_0_0
    GET /api/v2_0_0/workflows

    GET /api/v1/workflows       # same as v1_1_0
    GET /api/v1_1_0/workflows
    GET /api/v1_0_0/workflows

Non-versioned end-points provide for the latest version.

Versioning applies to all paths (REST and Socket.IO) except for the paths that serve the frontend (`/`, `/edit`, `/monitor`).

When applying changes, increment the version semantically:

* major: breaking API changes
* minor: API has extra stuff
* patch: same API, only bug fix
