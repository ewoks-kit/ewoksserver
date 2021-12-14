import sys
import flask
from contextlib import contextmanager
from flask_restful import Api
from flask_cors import CORS

from ..resources import workflows
from ..resources import tasks
from ..ewoks import execution


def _add_resources(app: flask.Flask):
    api = Api(app)
    api.add_resource(workflows.Workflows, "/workflows")
    api.add_resource(workflows.Workflow, "/workflow/<workflow_id>")
    
    api.add_resource(workflows.Execute, "/workflow/execute")
    
    api.add_resource(tasks.Tasks, "/tasks")
    api.add_resource(tasks.Task, "/task/<task_id>")


def create_app() -> flask.Flask:
    app = flask.Flask(__name__)
    cors = CORS(app)  # noqa F841
    app.config["CORS_HEADERS"] = "Content-Type"
    _add_resources(app)
    return app


@contextmanager
def _run_context(app: flask.Flask):
    with app.app_context():
        with execution.worker_pool() as workers:
            flask.g.workers = workers
            yield


def run_app(app: flask.Flask):
    with _run_context(app):
        app.run()


@contextmanager
def test_app(app: flask.Flask):
    with _run_context(app):
        with app.test_client() as client:
            yield client


def main():
    app = create_app()
    run_app(app)


if __name__ == "__main__":
    sys.exit(main())
