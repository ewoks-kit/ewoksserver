ewoksserver |version|
=====================

*ewoksserver* is a Python project that can be used in two ways:

- as **a full-stack web application** to create, modify and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows through `ewoksweb <https://ewoksweb.readthedocs.io/>`_ .
- as **a REST server** to manage and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows.

See the relevant section of the documentation below for each usecase.

*ewoksserver* is developed by the `Software group <http://www.esrf.eu/Instrumentation/software>`_ of the `European Synchrotron <https://www.esrf.eu/>`_.

Use as a full-stack web application
-----------------------------------

To use *ewoksserver* to create, modify and execute workflows, first install it with the ``frontend`` (i.e. *ewoksweb*)

.. code:: bash

    pip install ewoksserver[frontend]

Then, start the full-stack app

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


Use as a REST server
--------------------

To start the REST server, the ``frontend`` requirements are not needed:

.. code:: bash

    pip install ewoksserver

The server can then be started the same way

.. code:: bash

    ewoks-server

``--dir`` and ``--port`` command line arguments are available to respectively change the resource directory and the port. To have the complete list of arguments, run

.. code::bash
    
    ewoks-server --help

To go further, see the following pages

.. toctree::
    :maxdepth: 1
    :caption: REST server

    configuration
    restapi
    restapi_versioning
    api
