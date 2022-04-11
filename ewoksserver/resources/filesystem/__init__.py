import flask
from flask_restful import Api
from . import tasks
from . import workflows


def add_file_resources(app: flask.Flask):
    api = Api(app)

    # Save/load/execute workflows
    api.add_resource(workflows.Workflows, "/workflows")
    api.add_resource(workflows.Workflow, "/workflow/<identifier>")
    api.add_resource(workflows.Execute, "/workflows/execute")

    # Save/load tasks
    api.add_resource(tasks.Tasks, "/tasks")
    api.add_resource(tasks.Task, "/task/<identifier>")
    api.add_resource(tasks.Descriptions, "/tasks/descriptions")
    api.add_resource(tasks.DiscoverTasks, "/tasks/discover")
