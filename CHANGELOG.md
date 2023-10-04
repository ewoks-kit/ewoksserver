# CHANGELOG.md

## 0.6.0 (unreleased)

## 0.5.0

Changes:
  - `GET /workflows`: optional `keywords` to filter the workflows
  - `GET /workflows/descriptions`: optional `keywords` to filter the workflows
  - `GET /workflows/descriptions`: result `EwoksGraphDescriptionSchema` changed. It may include
     keywords, input_schema and ui_schema.
  - `/workflow/{identifier}` and `/workflows`: the `EwoksGraphSchema` did not change but
    the `graph` field may now contain the following extra keys: keywords, input_schema, ui_schema,
    execute_parameters and worker_options.
  - The `execute_parameters` and `worker_options` field from the workflow are merged with the
    equivalent dictionaries provided by the client when calling `POST /execute/{identifier}`

## 0.4.0

Bug fixes:
  - Trying to delete a non-existing entity now returns 404

Changes:
  - Default resources are now copied in the launched server resource directory

## 0.3.3

Bug fixes:
  - Fix bug with absolute configuration filename

Changes:
  - Logs: celery and ewoks configurations could be empty dictionaries

## 0.3.2

Changes:
  - Allow to run the `socketio` server in production environments

## 0.3.1

Bug fixes:
  - GET /execution/events: event grouping per job failed in case of parallel workflows

## 0.3.0

New features:
  - CLI "host" argument (to allow external access)

## 0.2.0

New features:
  - Task discovery in local or celery workers
  - Automatic task discovery without specifying modules
  - Optional automatic task discovery when starting the server

## 0.1.1

Changes:
  - Only enforce the configuration with --frontend-tests
  - Allow task discovery to change existing resources

## 0.1.0

Added:
  - REST API to load and store ewoks workflows
  - REST API to load and store ewoks tasks
  - REST API to execute workflows with ewoksjob
  - REST API to query ewoks execution events
  - Websocket API to ewoks execution events
  - Serve ewoksweb frontend
  - Swagger API documentation
