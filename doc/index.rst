ewoksserver |release|
=====================

*ewoksserver* is a REST server to manage and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows.

It serves as a backend for `ewoksweb <https://ewoksweb.readthedocs.io/>`_ and emits execution events over *websocket*.

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

Run the tests

.. code:: bash

    pip install ewokserver[test]
    pytest --pyargs ewokserver.tests

Documentation
-------------

.. toctree::
    :maxdepth: 2

    restapi
    api
