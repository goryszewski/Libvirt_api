from .vms import VirtualMachines,VirtualMachine
from .task import Tasks,Task

def initialize_routes(api):
    api.add_resource(VirtualMachines, "/api/vms")
    api.add_resource(Tasks, "/api/tasks")
    api.add_resource(Task, "/api/task/<id>")
