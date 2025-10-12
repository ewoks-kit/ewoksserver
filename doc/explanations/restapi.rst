REST API versioning
-------------------

By default the server provides versioned end-points for all full and major versions. For example

.. code-block::

    GET /api/workflows          # same as v2_0_0

    GET /api/v2/workflows       # same as v2_0_0
    GET /api/v2_0_0/workflows

    GET /api/v1/workflows       # same as v1_1_0
    GET /api/v1_1_0/workflows
    GET /api/v1_0_0/workflows

Non-versioned end-points provide for the latest version.
