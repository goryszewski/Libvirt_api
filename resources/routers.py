from .vms import VirtualMachines

def initialize_routes(api):
    api.add_resource(VirtualMachines, "/api/vms")