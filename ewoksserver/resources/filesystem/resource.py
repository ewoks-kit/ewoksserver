from pprint import pformat
from typing import List, Union, Tuple
from flask import request
from flask import current_app
from flask_restful import reqparse, Resource
from . import utils


class BaseFileResource(Resource):
    """Base class without end points"""

    RESOURCE_TYPE = NotImplemented

    @property
    def root_url(self) -> utils.ResourceUrlType:
        return utils.root_url(
            current_app.config.get("RESOURCE_DIRECTORY"), self.RESOURCE_TYPE + "s"
        )

    def save_resource(
        self, resource: utils.ResourceType, overwrite=False
    ) -> Tuple[Union[str, utils.ResourceType, utils.ResourceIdentifierType], int]:
        """Returns

        - ResourceIdentifierType, 200 (overwrite=True)
        - ResourceType, 200 (overwrite=False)
        - str, 403
        - str, 500
        """
        try:
            identifier = self.get_identifier(resource)
        except Exception as e:
            return (
                f"failed to extract {self.RESOURCE_TYPE} identifier from '{resource}': {e}",
                500,
            )
        root_url = self.root_url
        if not overwrite and utils.resource_exists(root_url, identifier):
            return (
                f"{self.RESOURCE_TYPE.capitalize()} '{identifier}' exists. Please change identifier and retry.",
                403,
            )
        try:
            utils.save_resource(root_url, identifier, resource)
        except OSError as e:
            return f"{self.RESOURCE_TYPE} '{identifier}' save error: {e}", 500
        if overwrite:
            return identifier, 200
        else:
            return resource, 200

    def load_resource(
        self,
        identifier: utils.ResourceIdentifierType,
    ) -> Tuple[Union[utils.ResourceType, str], int]:
        """Returns

        - ResourceType, 200
        - str, 403
        - str, 404
        - str, 500
        """
        try:
            return utils.load_resource(self.root_url, identifier), 200
        except FileNotFoundError:
            return f"{self.RESOURCE_TYPE} '{identifier}' does not exist", 404
        except PermissionError:
            return (
                f"no permission to access {self.RESOURCE_TYPE} '{identifier}'",
                403,
            )
        except OSError as e:
            return f"{self.RESOURCE_TYPE} '{identifier}' loading error: {e}", 500

    def delete_resource(
        self, identifier: utils.ResourceIdentifierType
    ) -> Tuple[utils.ResourceIdentifierType, int]:
        """Returns

        - ResourceIdentifierType, 200
        - str, 500
        """
        try:
            utils.delete_resource(self.root_url, identifier)
        except OSError as e:
            return f"{self.RESOURCE_TYPE} '{identifier}' delete error: {e}", 500
        return identifier, 200

    def list_resources(self) -> Tuple[List[utils.ResourceIdentifierType], int]:
        resources = list(utils.resource_identifiers(self.root_url))
        return resources, 200

    def get_identifier(
        self, resource: utils.ResourceType
    ) -> utils.ResourceIdentifierType:
        raise NotImplementedError


class FileResource(BaseFileResource):
    """End points

    GET /<endpoint>/<identifier>
        ResourceType, 200
        str, 404
        str, 403
        str, 500

    PUT /<endpoint>/<identifier>
        ResourceIdentifierType, 200
        str: 400
        str: 403
        str, 500

    DELETE /<endpoint>/<identifier>
        ResourceIdentifierType, 200
        str, 500
    """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def get(
        self, identifier: utils.ResourceIdentifierType
    ) -> Tuple[Union[utils.ResourceType, str], int]:
        current_app.logger.debug("GET /%s/%s", self.endpoint, identifier)
        return self.load_resource(identifier)

    def put(
        self, identifier: utils.ResourceIdentifierType
    ) -> Tuple[Union[str, utils.ResourceType, utils.ResourceIdentifierType], int]:
        root_url = self.root_url
        resource = request.json
        current_app.logger.debug(
            "PUT /%s/%s\n ROOT_URL = %s\n ARGS = %s\n REQUEST = %s",
            self.endpoint,
            identifier,
            root_url,
            pformat(self.reqparse.parse_args()),
            pformat(resource),
        )
        try:
            ridentifier = self.get_identifier(resource)
        except Exception as e:
            return (
                f"failed to extract {self.RESOURCE_TYPE} identifier from '{resource}': {e}",
                500,
            )
        if identifier != ridentifier:
            return (
                f"resource identifier {identifier} is not equal to {ridentifier}",
                400,
            )
        return self.save_resource(resource, overwrite=True)

    def delete(
        self, identifier: utils.ResourceIdentifierType
    ) -> Tuple[utils.ResourceIdentifierType, int]:
        current_app.logger.debug("DELETE /%s/%s", self.endpoint, identifier)
        return self.delete_resource(identifier)


class FileResources(BaseFileResource):
    """End points

    GET /<endpoint>
        List[ResourceIdentifierType], 200

    POST /<endpoint>
        ResourceType, 200
        str, 403
        str, 500
    """

    def get(self) -> List[utils.ResourceIdentifierType]:
        current_app.logger.debug("GET /%s", self.endpoint)
        return self.list_resources()

    def post(
        self,
    ) -> Tuple[Union[str, utils.ResourceType, utils.ResourceIdentifierType], int]:
        root_url = self.root_url
        resource = request.json
        current_app.logger.debug(
            "POST /%s\n ROOT_URL = %s\n REQUEST = %s",
            self.endpoint,
            root_url,
            pformat(resource),
        )
        return self.save_resource(resource, overwrite=False)
