Configure ``ewoksserver``
=======================

``ewoksserver`` can be configured by declaration the following variables in a Python file:

- ``RESOURCE_DIRECTORY`` (string): defines the path to the resource folder where workflows, tasks, icons are stored. Equivalent to the ``--dir/-d`` command line argument.
- ``EWOKS`` (dict): Configuration of ewoks handlers. See the `Ewoks events`_ section below.
- ``CELERY`` (dict): Configuration of Celery to allow launching workflows in ewoks workers.

*Example*:

.. code:: python
    
    # /tmp/config.py

    RESOURCE_DIRECTORY = "/path/to/resource/directory/"

    EWOKS = {"handlers": ...}

    CELERY = {"broker_url":...}


The path to configuration file can then be passed through the ``--config/-c`` command line argument:

.. code:: bash

    ewoks-server --config /tmp/config.py

The environment variable ``EWOKSSERVER_SETTINGS`` can be used instead:

.. code:: bash

    export EWOKSSERVER_SETTINGS=/tmp/config.py
    ewoks-server



Ewoks events
------------

When executing workflows, ``ewoksserver`` can send ewoks events through a websocket. Events are stored in a database by ``ewoksjob`` which needs further configuration.

``ewoksjob`` supports ``redis`` and ``sql`` as databases. So first, one of these must be installed (here we choose ``sql``):

.. code:: bash

    pip install ewoksjob[sql]

Then, in the configuration of ``ewoks-server``, the ``EWOKS`` handler must be appropriately set:

.. code:: python

    # /tmp/config.py

    EWOKS = {
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

If the server displays on start-up that the ``EWOKS`` handlers are properly set, it means that ewoks events are ready to be sent when executing workflows:

.. code:: bash

    $ ewoks-server -c /tmp/config.py

    <...>

    EWOKS:
    {'handlers': [{'arguments': [{'name': 'uri',
                                'value': 'file:/home/huder/ewoksserver_resources/ewoks_events.db'}],
                'class': 'ewokscore.events.handlers.Sqlite3EwoksEventHandler'}]}

    <...>


