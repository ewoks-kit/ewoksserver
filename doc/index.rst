ewoksserver |version|
=====================

*ewoksserver* is a REST server to manage and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows.

It serves as a backend for `ewoksweb <https://ewoksweb.readthedocs.io/>`_ and emits execution events over *Socket.IO*.

*ewoksserver* has been developed by the `Software group <http://www.esrf.eu/Instrumentation/software>`_ of the `European Synchrotron <https://www.esrf.eu/>`_.

Getting started
---------------

Install requirements

.. code:: bash

    pip install ewokserver[frontend]

Start the REST server which also serves the frontend

.. code:: python

    ewoks-server

or for an installation with the system python

.. code:: bash

    python3 -m ewoksserver.server


.. note::

    ``ewoks-server`` takes the port 5000 by default. If there are other applications running on this port (e.g. Airplay on Mac), another port can be chosen

    .. code:: bash

        ewoks-server -p 6666


Documentation
-------------

.. toctree::
    :maxdepth: 2

    configuration
    restapi
    api
