from . import resource
from .. import api

class IconsJson(resource.JsonResource):
    RESOURCE_TYPE = "icon"

    def get_identifier(
        self, resource: resource.ResourceContentType
    ) -> resource.ResourceIdentifierType:
        # print(resource)
        return resource["name"]

    @api.list_resource_identifiers("icon")
    def get(self) -> resource.ResponseType:
        print('send the descriptions from JSON')
        return self.list_resource_identifiers()
