# CHANGELOG.md

## Unreleased

- Pin `ewoksjob` requirement to `1.x`.

## 2.0.1

- Pin `ewoksjob` requirement to `0.x`.

## 2.0.0

New API version `v2_0_0`:

- End-point `/execution/events` returns events with the field `engine` instead of `binding`.
- End-point `/execution/workers` is renamed to `/execution/queues`.
- End-point `/execute/{identifier}` payload field `worker_options` is renamed `submit_arguments`. This renaming also impacts the related workflow field that is merged with the payload: if a workflow contain the field `worker_options` in its `graph` section, it needs to be renamed to `submit_arguments` when using the v2 API.

Breaking changes:

- Tasks are rediscovered when launching the server. This can be disabled by using the CLI arg `--no-discovery-at-launch`.
- `--rediscover-tasks` CLI argument was removed.

## 1.4.1

Bug fixes:

- Ignore unknown dotenv variables.

## 1.4.0

New features:

- New setting `EWOKS_DISCOVERY` in the server config. It is a dictionnary with two fields:
  - `on_start_up` (bool): rediscover tasks when restarting the server
  - `timeout` (number): timeout for task discovery operations (replaces `DISCOVER_TIMEOUT` that is now deprecated)
- Support the Uvicorn and FastAPI command line interfaces to start the server.
- New end-point `/execution/workers` to get all task execution queue names.
- End-point `/tasks/discover` now has an `task_type` option and discovers all task types when not provided.

Changes:

- `EWOKS` configuration field was renamed `EWOKS_EXECUTION` (`EWOKS_EXECUTION` is now deprecated).
- Documentation end-point has been renamed from `/api/docs` to `docs`.

Bug fixes:

- Handle remote task discovery failures.
- Fix end-point `/execute/{identifier}` documentation of the identifier.

## 1.3.0

Changes:

- Task discovery is now done in all available queues if `CELERY` is set-up. It was only done in the default queue `celery` before.
- New setting `DISCOVER_TIMEOUT` in the server config: it allows to set a timeout for task discovery operations (default: `None` i.e. no timeout).
- Improve Celery config print on start-up

Bug fixes:

- Fix task discovery if no module is supplied

## 1.2.0

Changes:

- `ewoksweb` is no longer installed with `ewoksserver[frontend]`.
  Instead `ewoksserver[frontend]` is a dependency of `ewoksweb`.

Bug fixes:

- Support pip 24.1 and avoid pyyaml 6.0.2rc1
- Ignore malformed tasks in the resource directory

## 1.1.0

New API version `v1_1_0`:

- New endpoint `GET /api/execution/workers` to retrieve the list of workers if Celery is set-up (`null` otherwise).

## 1.0.0

Migrate to FastAPI

- Endpoints are now prefixed with `/api` (e.g. `/workflows` becomes `/api/workflows`)
- Introduces API versioning (`/api` prefix uses the latest version, `/api/v1` uses the latest v1, `/api/v1_0_0` uses the specific 1.0.0 version )
- Default port changed to `5000`
- Changes to the command-line interface (`-c` is now `--config`, `-d` is now `--dir`, ...)

See [this page](https://gitlab.esrf.fr/workflow/ewoks/ewoksserver/-/merge_requests/97) for the full changes brought by this migration.

## 0.5.0

Changes:

- `GET /workflows`: optional `keywords` to filter the workflows
- `GET /workflows/descriptions`: optional `keywords` to filter the workflows
- `GET /workflows/descriptions`: result `EwoksGraphDescriptionSchema` changed. It may include
  `keywords`, `input_schema` and `ui_schema`.
- `/workflow/{identifier}` and `/workflows`: the `EwoksGraphSchema` did not change but
  the `graph` field may now contain the following extra keys: `keywords`, `input_schema`,
  `ui_schema`, `execute_parameters` and `worker_options`.
- The `execute_parameters` and `worker_options` fields from the workflow are merged with the
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
