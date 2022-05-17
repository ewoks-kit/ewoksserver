from . import resource
from .. import api
from flask import Response

class Icon(resource.BinaryResource):
    RESOURCE_TYPE = "icon"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["name"]

    @api.get_resource("icon")
    def get(self, identifier: resource.ResourceIdentifierType) -> resource.ResourceIdentifierType:
        ret = self.load_resource(identifier)
        print('from icons to be send', ret)
        return Response(ret[0], mimetype='image/svg+xml')
        # return ret

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

    @api.list_resource_content("icon")
    def get(self):
        return self.list_resource_content()
