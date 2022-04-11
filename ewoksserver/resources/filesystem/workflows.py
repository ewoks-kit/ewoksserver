from pprint import pformat
import flask
from flask import request
from flask import current_app
from ewoks import execute_graph
from . import utils
from . import resource


class Workflow(resource.FileResource):
    RESOURCE_TYPE = "workflow"

    def get_identifier(
        self, resource: utils.ResourceType
    ) -> utils.ResourceIdentifierType:
        return resource["graph"]["id"]


class Workflows(resource.FileResources):
    RESOURCE_TYPE = "workflow"

    def get_identifier(
        self, resource: utils.ResourceType
    ) -> utils.ResourceIdentifierType:
        return resource["graph"]["id"]


class Execute(resource.Resource):
    """End points

    POST /<endpoint>
        dict, 200
        str, 500
    """

    def post(self):
        request_data = request.json
        current_app.logger.debug("POST /%s:\n%s", self.endpoint, pformat(request_data))
        workers = flask.g.get("workers", None)
        if workers is None:
            return "fask app does not have workers", 500
        workers.submit(execute_graph, **request_data)
        return request_data, 200
