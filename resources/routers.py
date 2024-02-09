from .vms import VirtualMachines, VirtualMachine, Cloud
from .task import Tasks, Task
from .interfaces import Interface
from .hdd import Hdd
from .loadbalancer import Loadbalancer, Loadbalancers

from .k8s import Node, Lb, Lbtest


def initialize_routes(api):
    api.add_resource(Cloud, "/api/cloud/vms")

    api.add_resource(Hdd, "/api/hdd/<vmid>")
    api.add_resource(Interface, "/api/interface/<vmid>")

    api.add_resource(VirtualMachines, "/api/vms")
    api.add_resource(VirtualMachine, "/api/vm/<id>")

    api.add_resource(Loadbalancers, "/api/lbs")
    api.add_resource(Loadbalancer, "/api/lb/<id>")

    api.add_resource(Tasks, "/api/tasks")
    api.add_resource(Task, "/api/task/<id>")

    # /api/v1/k8s/node
    api.add_resource(Node, "/api/v1/k8s/node")
    # /api/v1/k8s/lb
    api.add_resource(Lb, "/api/v1/k8s/lb")
    api.add_resource(Lbtest, "/api/v1/k8s/lb/<ip>")
