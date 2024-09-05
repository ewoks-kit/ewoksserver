# Developer information

## General guidelines

<a href="https://gitlab.esrf.fr/dau/ci/pyci/-/blob/main/CONTRIBUTING.md" target="_blank">CONTRIBUTING.md</a>

## Starting the server

A custom command line interface is provided to start the application

.. code:: bash

    ewoks-server

The Uvicorn and FastAPI command line interface are supported as well

.. code:: bash

    uvicorn ewoksserver.main:app
    uvicorn --factory ewoksserver.app:create_app
    fastapi dev src/ewoksserver/main.py
    fastapi run src/ewoksserver/main.py

Ewoks specific application parameters (as opposed to FastAPI or Uvicorn parameters)
can be provided through (in order of priority)

* command line interface arguments (example: `--rediscover-tasks`, only available for `ewoks-server`)
* environment variables (example: `EWOKSAPP_REDISCOVER_TASKS=True`)
* "dotenv" file called `.env.prod` in the current working directory
* "dotenv" file called `.env` in the current working directory

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
