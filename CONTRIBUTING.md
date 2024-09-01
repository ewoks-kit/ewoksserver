# Developer information

## General guidelines

<a href="https://gitlab.esrf.fr/dau/ci/pyci/-/blob/main/CONTRIBUTING.md" target="_blank">CONTRIBUTING.md</a>

## Starting the server

To allow for custom command line arguments, an entry point is created to start the server

.. code:: bash

    ewoks-server

If none of the ewoks specific parameters like `--rediscover-tasks` need to be specified you
can also do this

.. code:: bash

    uvicorn --factory ewoksserver.app:create_app

Ewoksserver also provides support for the canonical way of starting a FastAPI application.
This requires a module with a global FastAPI instance, which is then referenced like this

.. code:: bash

    uvicorn ewoksserver.main:app

Using the FastAPI CLI the command looks like this

.. code:: bash

    fastapi dev src/ewoksserver/main.py
    fastapi run src/ewoksserver/main.py

When using the native Uvicorn or FastAPI CLI, ewoks specific parameters parameters like
`--rediscover-tasks` are supported through environment variables with prefix `EWOKSAPP_`
like `EWOKSAPP_REDISCOVER_TASKS=True`.

## API versioning

Versioning applies to all paths under the `/api` subpath (REST and Socket.IO). This does not include paths that serve the frontend (`/`, `/edit`, `/monitor`).

When applying changes, increment the version semantically:

- major: breaking API changes
- minor: API has extra stuff
- patch: same API, only bug fix

## Documentation

Documentation is generated with Sphinx. Before running any Sphinx command, generate the `spec.json` file via:

```
ewoks-server-spec doc/spec.json
```

This will be used to generate the Redoc page documentation of the REST API. Then, the Sphinx doc can be generated as usual:

```
sphinx-build doc build/sphinx/html -E -a
```
