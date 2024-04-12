ewoksserver |version|
=====================

*ewoksserver* is a **a REST server** to manage and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows.

It serves as a backend for `ewoksweb <https://ewoksweb.readthedocs.io/>`_, **a full-stack web application** to create, modify and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows.

> If you are looking for information on `ewoksweb`, please refer to the `ewoksweb <https://ewoksweb.readthedocs.io/>`_ documentation.

*ewoksserver* is developed by the `Software group <http://www.esrf.eu/Instrumentation/software>`_ of the `European Synchrotron <https://www.esrf.eu/>`_.

Usage
-----

To start the REST server, first install it via `pip`:

.. code:: bash

    pip install ewoksserver

The server can then be started via

.. code:: bash

    ewoks-server


The web app will be available at ``localhost:8000``.

.. note::

    ``ewoks-server`` takes the port 8000 by default. If there are other applications running on this port (e.g. iTunes radio on Mac), another port can be chosen

    .. code:: bash

        ewoks-server --port 6660

    Also by default, ``ewoks-server`` will save ewoks resources (workflows, tasks, icons) in the current folder. This can be changed through the ``--dir`` command line argument

    .. code:: bash

        ewoks-server --dir /path/to/ewoksserver/resources

    To have the complete list of arguments, run

    .. code::bash
        
        ewoks-server --help

To go further 
-------------

See the following pages

.. toctree::
    :maxdepth: 1
    :caption: REST server

    configuration
    restapi
    restapi_versioning
    api

