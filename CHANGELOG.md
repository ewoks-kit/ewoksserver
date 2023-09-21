# CHANGELOG.md

## 0.4.0 (unreleased)

## 0.3.3 (unreleased)

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
