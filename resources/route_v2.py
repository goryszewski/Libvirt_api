from .bind import BindHddResource
from .hdd import HddResource

def initv2(api):
    api.add_resource(HddResource, "/api/v2/hdd", "/api/v2/hdd/<id>")
    api.add_resource(BindHddResource, "/api/v2/hdd/<hdd_id>/vm/<vm_id>")
