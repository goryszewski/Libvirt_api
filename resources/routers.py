from .vms import  VirtualMachine, Cloud
from .task import Tasks, Task
from .interfaces import Interface
from .hdd import HddR
from .loadbalancer import Loadbalancer, Loadbalancers

from.network import NetworkResource

from .auth import LoginApi

from .k8s import Node, Lb
from .user import Users,User


def initialize_routes(api):
    api.add_resource(Cloud, "/api/cloud/vms")

    api.add_resource(HddR, "/api/hdd/<vmid>")
    api.add_resource(Interface, "/api/interface/<vmid>")

    api.add_resource(VirtualMachine, "/api/vm","/api/vm/<id>")
    api.add_resource(NetworkResource, "/api/network","/api/network/<id>")

    api.add_resource(Loadbalancers, "/api/lbs")
    api.add_resource(Loadbalancer, "/api/lb/<id>")

    api.add_resource(Tasks, "/api/tasks")
    api.add_resource(Task, "/api/task/<id>")

    api.add_resource(Users, "/api/users")
    api.add_resource(User, "/api/user/<id>")

    # /api/v1

    api.add_resource(LoginApi, "/api/v1/auth")
    # /api/v1/k8s/node
    api.add_resource(Node, "/api/v1/k8s/node")
    # /api/v1/k8s/lb

    api.add_resource(Lb, "/api/v1/k8s/lb", "/api/v1/k8s/lb/<ip>")
