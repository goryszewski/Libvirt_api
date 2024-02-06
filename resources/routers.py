from .vms import VirtualMachines, VirtualMachine, Cloud
from .task import Tasks, Task
from .interfaces import Interface
from .hdd import Hdd
from .loadbalancer import Loadbalancer,Loadbalancers


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
