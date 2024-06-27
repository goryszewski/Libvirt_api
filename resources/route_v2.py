from .hdd import HddResource
from .node import V2_NodeBindDisk
from .node import V2_Node
from .metadata import V2_Metadata


def initv2(api):
    api.add_resource(HddResource, "/api/v2/hdd", "/api/v2/hdd/<id>")

    api.add_resource(
        V2_NodeBindDisk, "/api/v2/node/<name>/hdd/<hdd_id>", "/api/v2/node/<name>/hdd"
    )
    api.add_resource(V2_Node, "/api/v2/node/<name>", "/api/v2/node")
    api.add_resource(V2_Metadata, "/api/v2/metadata")
