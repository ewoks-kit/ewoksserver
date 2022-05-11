from . import resource
from .. import api


class Icon(resource.JsonResource):
    RESOURCE_TYPE = "icon"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["name"]

    @api.get_resource("icon")
    def get(self, identifier: resource.ResourceIdentifierType) -> resource.ResponseType:
        return self.load_resource(identifier)

    @api.put_resource("icon")
    def put(
        self, identifier: resource.ResourceIdentifierType, **resource
    ) -> resource.ResponseType:
        return self.save_resource(
            resource, error_on_missing=True, identifier=identifier
        )

    @api.delete_resource("icon")
    def delete(
        self, identifier: resource.ResourceIdentifierType
    ) -> resource.ResponseType:
        return self.delete_resource(identifier)


class Icons(resource.JsonResource):
    RESOURCE_TYPE = "icon"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["name"]

    @api.list_resource_identifiers("icon")
    def get(self) -> resource.ResponseType:
        return self.list_resource_identifiers()

    @api.post_resource("icon")
    def post(self, **resource) -> resource.ResponseType:
        return self.save_resource(resource, error_on_exists=True)


class Descriptions(resource.JsonResource):
    RESOURCE_TYPE = "icon"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        return resource["name"]

    @api.list_resource_content("icon")
    def get(self):
        return self.list_resource_content()
