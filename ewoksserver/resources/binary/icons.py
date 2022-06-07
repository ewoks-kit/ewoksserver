import os
from . import resource
from .. import api
from flask import Response

class Icon(resource.BinaryResource):
    RESOURCE_TYPE = "icon"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["name"]

    @api.get_resource_binary("icon")
    def get(self, identifier: resource.ResourceIdentifierType) -> resource.ResourceIdentifierType:
        ret = self.load_resource(identifier)
        name, extension = os.path.splitext(identifier)

        mimeType = ''
        if extension == '.png':
            mimeType = 'image/png'
        elif extension == '.svg':
            mimeType = 'image/svg+xml'
        return Response(ret[0], mimetype=mimeType)

    @api.delete_resource("icon")
    def delete(
        self, identifier: resource.ResourceIdentifierType
    ) -> resource.FileResponseType:
        return self.delete_resource(identifier)


class Icons(resource.BinaryResource):
    RESOURCE_TYPE = "icon"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["name"]

    @api.list_resource_identifiers("icon")
    def get(self) -> resource.FileResponseType:
        return self.list_resource_identifiers()

    @api.upload_resource("icon")
    def post(self, **resource) -> resource.FileResponseType:
        return self.upload_resource(resource, error_on_exists=True)
