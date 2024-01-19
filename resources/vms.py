from flask_restful import Resource
import json
import libvirt, libxml2
from .Libvirt import Libvirt

class VirtualMachines(Resource):
    def __init__(self):
        self.libVirt = Libvirt()
    def get(self):
        vm = self.libVirt.get()
        return vm, 200
    
    def put(self):
        vm,e = self.libVirt.put()
        return vm ,e