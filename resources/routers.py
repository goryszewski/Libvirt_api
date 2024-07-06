from .network import NetworkResource
from .vms import VirtualMachineResource, Cloud
from .task import Tasks, Task
from .interfaces import InterfaceResource
from .loadbalancer import Loadbalancer
from .auth import LoginApi
from .user import Users, User
from .route_v2 import initv2


def initialize_routes(api):
    initv2(api=api)

    # V1
    api.add_resource(LoginApi, "/api/v1/auth")

    # api.add_resource(NetworkResource, "/api/v1/network", "/api/v1/network/<id>")
    # api.add_resource(Loadbalancer, "/api/v1/lb", "/api/v1/lb/<namespace>/<name>")
    #
    api.add_resource(NetworkResource, "/api/network", "/api/network/<id>")

    api.add_resource(Loadbalancer, "/api/lb", "/api/lb/<namespace>/<name>")

    api.add_resource(Cloud, "/api/cloud/vms")

    api.add_resource(InterfaceResource, "/api/interface/<vmid>")

    api.add_resource(VirtualMachineResource, "/api/vm", "/api/vm/<id>")

    api.add_resource(Tasks, "/api/tasks")
    api.add_resource(Task, "/api/task/<id>")

    api.add_resource(Users, "/api/users")
    api.add_resource(User, "/api/user/<id>")
