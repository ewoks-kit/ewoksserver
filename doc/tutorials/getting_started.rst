Getting started
===============

To start the REST server, first install it via `pip`:

.. code-block:: bash

    pip install ewoksserver

The server can then be started via

.. code-block:: bash

    ewoks-server

The web app will be available at ``localhost:8000``.

.. note::

    ``ewoks-server`` takes the port 8000 by default. If there are other applications running on this port (e.g. iTunes radio on Mac), another port can be chosen

    .. code-block:: bash

        ewoks-server --port 6660

    Also by default, ``ewoks-server`` will save ewoks resources (workflows, tasks, icons) in the current folder. This can be changed through the ``--dir`` command line argument

    .. code-block:: bash

        ewoks-server --dir /path/to/ewoksserver/resources

    To have the complete list of arguments, run

    .. code-block::bash
        
        ewoks-server --help
