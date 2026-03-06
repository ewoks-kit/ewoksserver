# ewoksserver

[![Pipeline](https://github.com/ewoks-kit/ewoksserveractions/workflows/test.yml/badge.svg?branch=main)](https://github.com/ewoks-kit/ewoksserveractions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/ewoks-kit/ewoksserver)](https://github.com/ewoks-kit/ewoksserverblob/main/LICENSE.md)
[![Coverage](https://codecov.io/gh/ewoks-kit/ewoksserverbranch/main/graph/badge.svg)](https://codecov.io/gh/ewoks-kit/ewoksserver)
[![Docs](https://readthedocs.org/projects/ewoksserverbadge/?version=latest)](https://ewoksserver.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/ewoksserver)](https://pypi.org/project/ewoksserver)

ewoksserver is a REST server to manage and execute [ewoks](https://ewoks.readthedocs.io/) workflows.

It serves as a backend for [ewoksweb](https://ewoksweb.readthedocs.io/) and emits ewoks execution events over Socket.IO.

## Getting started

Install the [ewoksserver](https://ewoksserver.readthedocs.io) Python package

```
pip install ewoksserver
```

## Development

Install from source

```bash
pip install -e .[dev]
```

Run tests

```bash
pytest
```

Launch the backend

```bash
ewoks-server
```

or for an installation with the system python

```bash
python3 -m ewoksserver.server
```

## Configuration

The configuration keys are uppercase variables in a python script:

```python
# /tmp/config.py
RESOURCE_DIRECTORY = "/path/to/resource/directory/"

EWOKS_EXECUTION = {"handlers": ...}

CELERY = {"broker_url":...}
```

Specify the configuration file through the CLI

```bash
ewoks-server --config /tmp/config.py
```

or using the environment variable EWOKSSERVER_SETTINGS

```bash
export EWOKSSERVER_SETTINGS=/tmp/config.py
ewoks-server
```

### Example

```python
import os

_SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

RESOURCE_DIRECTORY = os.path.join(_SCRIPT_DIR, "resources")

EWOKS_EXECUTION = {
    "handlers": [
        {
            "class": "ewokscore.events.handlers.Sqlite3EwoksEventHandler",
            "arguments": [
                {
                    "name": "uri",
                    "value": "file:" + os.path.join(_SCRIPT_DIR, "ewoks_events.db"),
                }
            ],
        }
    ]
}
```

## Documentation

https://ewoksserver.readthedocs.io/
