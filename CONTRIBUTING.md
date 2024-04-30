# Developer information

## General guidelines

<a href="https://gitlab.esrf.fr/dau/ci/pyci/-/blob/main/CONTRIBUTING.md" target="_blank">CONTRIBUTING.md</a>

## Starting the server

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

Ewoksserver does not provide this since a global app instance does not allow configuration before
instantiation and is impractical for unit testing.

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
