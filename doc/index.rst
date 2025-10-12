ewoksserver |version|
=====================

*ewoksserver* is a **a REST server** to manage and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows.

It serves as a backend for `ewoksweb <https://ewoksweb.readthedocs.io/>`_, **a full-stack web application**
to create, modify and execute `ewoks <https://ewoks.readthedocs.io/>`_ workflows.

*ewoksserver* is developed by the `Software group <http://www.esrf.eu/Instrumentation/software>`_
of the `European Synchrotron <https://www.esrf.eu/>`_.

.. admonition:: Quick Start

    .. code-block:: bash

        pip install ewoksserver

    The server can then be started via

    .. code-block:: bash

        ewoks-server

    The REST API (and the web app) will be available at ``localhost:8000``.

.. note::

    If you are looking information on the front-end, please refer to the
    `ewoksweb <https://ewoksweb.readthedocs.io/>`_ documentation.

.. toctree::
    :hidden:

    tutorials/index
    explanations/index
    reference/index
