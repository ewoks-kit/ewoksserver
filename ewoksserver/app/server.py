import sys
import flask
from contextlib import contextmanager
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import emit

# from flask_socketio import send
import time

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
        # app.run()

        socketio.run(app, port=5000)


@contextmanager
def test_app(app: flask.Flask):
    with _run_context(app):
        with app.test_client() as client:
            yield client


app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*")

# SocketIO Events


@socketio.on("connect")
def connected():
    print("Connected")


@socketio.on("disconnect")
def disconnected():
    print("Disconnected")


@socketio.on("Execute Graph")
def Execute(graph):
    print("Execute Graph")
    print(graph)

    executingEvents = [
        {
            "id": "1",
            "nodeId": "Prepare test set grid data",
            "event_type": "start",
            "values": {"a": 1, "b": 2},
            "executing": ["Prepare test set grid data"],
        },
        {
            "id": "2",
            "nodeId": "Prepare test set grid data",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3},
            "executing": [""],
        },
        {
            "id": "3",
            "nodeId": "EstTask_1",
            "event_type": "start",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["EstTask_1"],
        },
        {
            "id": "4",
            "nodeId": "CommonPrepareExperiment",
            "event_type": "start",
            "values": {"a": 1, "b": 2},
            "executing": ["CommonPrepareExperiment", "EstTask_1"],
        },
        {
            "id": "5",
            "nodeId": "EstTask_1",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["CommonPrepareExperiment"],
        },
        {
            "id": "6",
            "nodeId": "EstTask_0",
            "event_type": "start",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["EstTask_0", "CommonPrepareExperiment"],
        },
        {
            "id": "7",
            "nodeId": "CommonPrepareExperiment",
            "event_type": "stop",
            "values": {"a": 1, "b": 2},
            "executing": ["EstTask_0"],
        },
        {
            "id": "8",
            "nodeId": "Read and set grid data",
            "event_type": "start",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["EstTask_0", "Read and set grid data"],
        },
        {
            "id": "9",
            "nodeId": "EstTask_0",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": ["Read and set grid data"],
        },
        {
            "id": "10",
            "nodeId": "Read and set grid data",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3, "d": 4},
            "executing": [""],
        },
        {
            "id": "11",
            "nodeId": "Prepare test set grid data",
            "event_type": "start",
            "values": {"a": 1, "b": 2},
            "executing": ["Prepare test set grid data"],
        },
        {
            "id": "12",
            "nodeId": "Prepare test set grid data",
            "event_type": "stop",
            "values": {"a": 1, "b": 2, "c": 3},
            "executing": [""],
        },
    ]

    for ev in executingEvents:
        print(ev)
        emit("Executing", ev, broadcast=True)
        time.sleep(4)  # * random.seed(float(ev.id))


def main():
    # app = create_app()
    run_app(app)


if __name__ == "__main__":
    sys.exit(main())
