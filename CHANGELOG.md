# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.1.2] - 2026-03-06

### Changed

- Project migrated to https://github.com/ewoks-kit/ewoksserver.

## [2.1.1] - 2025-08-02

## Fixed

- Allow to server to start when task discovery fails.

## [2.1.0] - 2025-07-28

### Changed

- Pin `ewoksjob` requirement to `1.x`.

## [2.0.1] - 2025-04-29

### Changed

- Pin `ewoksjob` requirement to `0.x`.

## [2.0.0] - 2025-01-22

### Changed

- Tasks are rediscovered when launching the server. This can be disabled by using the CLI arg `--no-discovery-at-launch`.
- End-point `/execution/events` returns events with the field `engine` instead of `binding`.

### Removed

- `--rediscover-tasks` CLI argument was removed.
- End-point `/execution/workers` is renamed to `/execution/queues`.
- End-point `/execute/{identifier}` payload field `worker_options` is renamed `submit_arguments`. This renaming also impacts
  the related workflow field that is merged with the payload: if a workflow contain the field `worker_options` in its `graph`
  section, it needs to be renamed to `submit_arguments` when using the v2 API.

### Added

- New API version `v2_0_0`:

## [1.4.1] - 2024-12-21

### Fixed

- Ignore unknown dotenv variables.

## [1.4.0] - 2024-12-21

### Added

- New setting `EWOKS_DISCOVERY` in the server config. It is a dictionnary with two fields:
  - `on_start_up` (bool): rediscover tasks when restarting the server.
  - `timeout` (number): timeout for task discovery operations (replaces `DISCOVER_TIMEOUT` that is now deprecated).
- Support the Uvicorn and FastAPI command line interfaces to start the server.
- New end-point `/execution/workers` to get all task execution queue names.
- End-point `/tasks/discover` now has an `task_type` option and discovers all task types when not provided.

### Changed

- `EWOKS` configuration field was renamed `EWOKS_EXECUTION` (`EWOKS_EXECUTION` is now deprecated).
- Documentation end-point has been renamed from `/api/docs` to `docs`.

### Fixed

- Handle remote task discovery failures.
- Fix end-point `/execute/{identifier}` documentation of the identifier.

## [1.3.0] - 2024-08-02

### Changed

- Task discovery is now done in all available queues if `CELERY` is set-up. It was only done in the default queue `celery` before.
- New setting `DISCOVER_TIMEOUT` in the server config: it allows to set a timeout for task discovery operations (default: `None` i.e. no timeout).
- Improve Celery config print on start-up.

### Fixed

- Fix task discovery if no module is supplied.

## [1.2.0] - 2024-06-23

### Changed

- `ewoksweb` is no longer installed with `ewoksserver[frontend]`.
  Instead `ewoksserver[frontend]` is a dependency of `ewoksweb`..

### Fixed

- Support pip 24.1 and avoid pyyaml 6.0.2rc1.
- Ignore malformed tasks in the resource directory.

## [1.1.0] - 2024-02-06

### Added

- New API version `v1_1_0`:
- New endpoint `GET /api/execution/workers` to retrieve the list of workers if Celery is set-up (`null` otherwise).

## [1.0.0] - 2023-12-06

### Changed

- Migrate to FastAPI.
- Endpoints are now prefixed with `/api` (e.g. `/workflows` becomes `/api/workflows`).
- Introduces API versioning (`/api` prefix uses the latest version, `/api/v1` uses the latest v1, `/api/v1_0_0` uses the specific 1.0.0 version ).
- Default port changed to `5000`.
- Changes to the command-line interface (`-c` is now `--config`, `-d` is now `--dir`, ...).

## [0.5.0] - 2023-10-04

### Changed

- `GET /workflows`: optional `keywords` to filter the workflows.
- `GET /workflows/descriptions`: optional `keywords` to filter the workflows.
- `GET /workflows/descriptions`: result `EwoksGraphDescriptionSchema` changed. It may include.
  `keywords`, `input_schema` and `ui_schema`.
- `/workflow/{identifier}` and `/workflows`: the `EwoksGraphSchema` did not change but
  the `graph` field may now contain the following extra keys: `keywords`, `input_schema`,
  `ui_schema`, `execute_parameters` and `worker_options`.
- The `execute_parameters` and `worker_options` fields from the workflow are merged with the
  equivalent dictionaries provided by the client when calling `POST /execute/{identifier}`.

## [0.4.0] - 2023-09-28

### Changed

- Default resources are now copied in the launched server resource directory.

### Fixed

- Trying to delete a non-existing entity now returns 404.

## [0.3.3] - 2023-09-21

### Changed

- Logs: celery and ewoks configurations could be empty dictionaries.

### Fixed

- Fix bug with absolute configuration filename.

## [0.3.2] - 2023-09-19

### Changed

- Allow to run the `socketio` server in production environments.

## [0.3.1] - 2023-09-18

### Fixed

- `GET /execution/events`: event grouping per job failed in case of parallel workflows.

## [0.3.0] - 2023-07-28

### Added

- CLI "host" argument (to allow external access).

## [0.2.0] - 2023-06-12

### Added

- Task discovery in local or celery workers.
- Automatic task discovery without specifying modules.
- Optional automatic task discovery when starting the server.

## [0.1.1] - 2023-06-09

### Changed

- Only enforce the configuration with --frontend-tests.
- Allow task discovery to change existing resources.

## [0.1.0] - 2023-06-01

### Added

- REST API to load and store ewoks workflows.
- REST API to load and store ewoks tasks.
- REST API to execute workflows with ewoksjob.
- REST API to query ewoks execution events.
- Websocket API to ewoks execution events.
- Serve ewoksweb frontend.
- Swagger API documentation.

[unreleased]: https://github.com/ewoks-kit/ewoksserver/compare/v2.1.2...HEAD
[2.1.2]: https://github.com/ewoks-kit/ewoksserver/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.com/ewoks-kit/ewoksserver/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/ewoks-kit/ewoksserver/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/ewoks-kit/ewoksserver/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/ewoks-kit/ewoksserver/compare/v1.4.1...v2.0.0
[1.4.1]: https://github.com/ewoks-kit/ewoksserver/compare/v1.4.0...v1.4.1
[1.4.0]: https://github.com/ewoks-kit/ewoksserver/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/ewoks-kit/ewoksserver/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/ewoks-kit/ewoksserver/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/ewoks-kit/ewoksserver/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ewoks-kit/ewoksserver/compare/v0.5.0...v1.0.0
[0.5.0]: https://github.com/ewoks-kit/ewoksserver/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/ewoks-kit/ewoksserver/compare/v0.3.3...v0.4.0
[0.3.3]: https://github.com/ewoks-kit/ewoksserver/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/ewoks-kit/ewoksserver/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/ewoks-kit/ewoksserver/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/ewoks-kit/ewoksserver/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ewoks-kit/ewoksserver/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/ewoks-kit/ewoksserver/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/ewoks-kit/ewoksserver/-/tags/v0.1.0
