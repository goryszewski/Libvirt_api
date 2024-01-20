from flask_restful import Resource
from flask import request

from .Libvirt import Libvirt
from Model.VMS import VMSchema

class VirtualMachines(Resource):
    def __init__(self):
        self.vm_schema = VMSchema()
        self.libVirt = Libvirt()
    def get(self):
        vm = self.libVirt.get()
        return vm, 200

    def post(self):
        payload= request.get_json()
        error = self.vm_schema.validate(payload)
        if error:
            return error, 422
        vm, code = self.libVirt.create(payload)
        return vm,code

    def delete(self,name):
        output = self.libVirt.delete(name)
        return output


class VirtualMachine(Resource):
    def __init__(self):
        self.vm_schema = VMSchema()
        self.libVirt = Libvirt()
    def get(self,name):
        vm = self.libVirt.get()
        return vm, 200


    def delete(self,name):
        output = self.libVirt.delete(name)
        return output
