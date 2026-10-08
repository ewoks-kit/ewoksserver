Server configuration
====================

``ewoksserver`` can be configured by declaration the following variables in a Python file:

- ``RESOURCE_DIRECTORY`` (string): defines the path to the resource folder where workflows,
  tasks, icons are stored. Equivalent to the ``--dir/-d`` command line argument.
- ``EWOKS_EXECUTION`` (dict): Configuration of ewoks handlers. See the `Ewoks events`_ section below.
- ``CELERY`` (dict): Configuration of Celery to allow launching workflows in ewoks workers.
- ``AUTH`` (dict): Authentication of REST requests. See the `Authentication`_ section below.

*Example*:

.. code-block:: python
    
    # /tmp/config.py

    RESOURCE_DIRECTORY = "/path/to/resource/directory/"

    EWOKS_EXECUTION = {"handlers": ...}

    CELERY = {"broker_url":...}


The path to configuration file can then be passed through the ``--config`` command line argument:

.. code-block:: bash

    ewoks-server --config /tmp/config.py

The environment variable ``EWOKSSERVER_SETTINGS`` can be used instead:

.. code-block:: bash

    export EWOKSSERVER_SETTINGS=/tmp/config.py
    ewoks-server



Authentication
--------------

Authentication is disabled by default. To enable it, define the ``AUTH`` variable in the configuration file:

.. code-block:: python

    AUTH = {
        "enabled": True,
        "secret_key": "<long random string>",
        "token_expire_minutes": 30,
        "users": {"alice": "<password hash>"},
    }

A password hash can be created with:

.. code-block:: bash

    python -c "from pwdlib import PasswordHash; print(PasswordHash.recommended().hash('<password>'))"

Clients get a token with ``POST /api/token`` (form fields ``username`` and ``password``)
and send it in the ``Authorization: Bearer <token>`` header.


Ewoks events
------------

When executing workflows, ``ewoksserver`` can send ewoks events through a Socket.IO connection.
Events are stored in a database by ``ewoksjob`` which needs further configuration.

``ewoksjob`` supports ``redis`` and ``sql`` as databases. So first, one of these must be installed
(here we choose ``sql``):

.. code-block:: bash

    pip install ewoksjob[sql]

Then, in the configuration of ``ewoks-server``, the ``EWOKS_EXECUTION`` parameter must define the
appropriate `"handlers"`:

.. code-block:: python

    # /tmp/config.py

    EWOKS_EXECUTION = {
        "handlers": [
            {
                "class": "ewokscore.events.handlers.Sqlite3EwoksEventHandler",
                "arguments": [
                    {
                        "name": "uri",
                        "value": "file:/any/path/ewoks_events.db",
                    }
                ],
            }
        ]
    }

If the server displays on start-up that the ``EWOKS_EXECUTION`` parameter has `"handlers"`,
it means that ewoks events are ready to be sent when executing workflows:

.. code-block:: bash

    $ ewoks-server -c /tmp/config.py

    <...>

    EWOKS_EXECUTION:
    {'handlers': [{'arguments': [{'name': 'uri',
                                'value': 'file:/home/huder/ewoksserver_resources/ewoks_events.db'}],
                'class': 'ewokscore.events.handlers.Sqlite3EwoksEventHandler'}]}

    <...>


