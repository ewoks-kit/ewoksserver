from pprint import pformat
from typing import Mapping
from flask import request
from flask import current_app
from ewokscore.task_summary import generate_task_summary
from . import utils
from . import resource


class Task(resource.FileResource):
    RESOURCE_TYPE = "task"

    def get_identifier(
        self, resource: utils.ResourceType
    ) -> utils.ResourceIdentifierType:
        return resource["task_identifier"]


class Tasks(resource.FileResources):
    RESOURCE_TYPE = "task"

    def get_identifier(
        self, resource: utils.ResourceType
    ) -> utils.ResourceIdentifierType:
        return resource["task_identifier"]


class Descriptions(resource.BaseFileResource):
    """
    GET: /<endpoint>
        List[ResourceType], 200
    """

    RESOURCE_TYPE = "task"

    def get_identifier(
        self, resource: utils.ResourceType
    ) -> utils.ResourceIdentifierType:
        return resource["task_identifier"]

    def get(self):
        current_app.logger.debug("GET /%s", self.endpoint)
        resources = list(utils.resources(self.root_url))
        return resources, 200


class DiscoverTasks(resource.BaseFileResource):
    """
    POST: /<endpoint>
        List[ResourceIdentifierType], 200
        str, 403
        str, 500
    """

    RESOURCE_TYPE = "task"

    def get_identifier(
        self, resource: utils.ResourceType
    ) -> utils.ResourceIdentifierType:
        return resource["task_identifier"]

    def post(self):
        root_url = self.root_url
        request_data = request.json
        current_app.logger.debug(
            "POST /%s\n ROOT_URL = %s\n REQUEST = %s",
            self.endpoint,
            root_url,
            pformat(request_data),
        )
        if not isinstance(request_data, Mapping):
            return
        module = request_data.get("module")
        if module:
            tasks = list(generate_task_summary(module))
        else:
            tasks = list()
        for _resource in tasks:
            response, code = self.save_resource(_resource, overwrite=False)
            if code != 200:
                return response, code
        tasks = [desc["task_identifier"] for desc in tasks]
        return tasks, 200
