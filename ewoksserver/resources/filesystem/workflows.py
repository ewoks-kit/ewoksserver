from pprint import pformat
from flask import request
from flask import current_app
from werkzeug.exceptions import HTTPException
from ewoksjob.client import submit, submit_local

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


class Execute(resource.BaseFileResource):
    RESOURCE_TYPE = "workflow"

    """End points
    POST /<endpoint>/<identifier>

        - job_id[str], 200
        - str, 403
        - str, 404
        - str, 500
    """

    def get_identifier(
        self, resource: utils.ResourceType
    ) -> utils.ResourceIdentifierType:
        return resource["graph"]["id"]

    def post(self, identifier: utils.ResourceIdentifierType):
        try:
            request_data = request.json
        except HTTPException:
            request_data = dict()
        else:
            if request_data is None:
                request_data = dict()
        current_app.logger.debug("POST /%s:\n%s", self.endpoint, pformat(request_data))
        graph, error_code = self.load_resource(identifier)
        if error_code != 200:
            return graph, error_code

        ewoks_config = current_app.config.get("EWOKS")
        if ewoks_config:
            execinfo = request_data.setdefault("execinfo", dict())
            handlers = execinfo.setdefault("handlers", list())
            for handler in ewoks_config.get("handlers", list()):
                if handler not in handlers:
                    handlers.append(handler)

        if current_app.config.get("CELERY") is None:
            future = submit_local(graph, **request_data)
            job_id = future.job_id
        else:
            future = submit(graph, **request_data)
            job_id = future.task_id
        return job_id, 200
