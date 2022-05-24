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
        print('-----from icons to be send', ret[0], identifier, os.path.splitext(identifier))
        name, extension = os.path.splitext(identifier)

        mimeType = ''
        if extension == '.png':
            mimeType = 'image/png'
        elif extension == '.svg':
            mimeType = 'image/svg+xml'
        print ('---------extension', extension, mimeType)
        return Response(ret[0], mimetype=mimeType)

    @api.put_resource("icon")
    def put(
        self, identifier: resource.ResourceIdentifierType, **resource
    ) -> resource.FileResponseType:
        return self.save_resource(
            resource, error_on_missing=True, identifier=identifier
        )

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
        # print(resource)
        return resource["name"]

    @api.list_resource_identifiers("icon")
    def get(self) -> resource.FileResponseType:
        print('-------send the descriptions from binary', self.list_resource_identifiers())

        return self.list_resource_identifiers()

    @api.post_resource("icon")
    def post(self, **resource) -> resource.FileResponseType:
        print(resource)
        return self.upload_resource(resource, error_on_exists=True)


class Descriptions(resource.BinaryResource):
    RESOURCE_TYPE = "icon"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["name"]

    # @api.list_resource_content("icon")
    # def get(self):
    #     return self.list_resource_content()
