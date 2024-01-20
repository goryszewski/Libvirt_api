from .vms import VirtualMachines,VirtualMachine

def initialize_routes(api):
    api.add_resource(VirtualMachines, "/api/vms")
    api.add_resource(VirtualMachine, "/api/vm/<name>")
