from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func

from Model.VMS import VirtualMachineSchema, VirtualMachine
from databases.db import db

class VirtualMachines(Resource):
    def __init__(self):
        self.vm_schema = VirtualMachineSchema()

    def get(self):
        vm = VirtualMachine.query.all()
        result = self.vm_schema.dump(vm)
        return result, 200

    def post(self):
        payload= request.get_json()
        error = self.vm_schema.validate(payload)
        if error:
            return error, 422

        vm = VirtualMachine.query.where(VirtualMachine.name == payload['name']).all()
        print(vm)
        if vm:
            vm = VirtualMachine.query.where(VirtualMachine.name == payload['name']).update(dict(**VirtualMachineSchema().load(payload), updatedAt=func.now()))
            print("update")
        else:
            vm = VirtualMachine(**self.vm_schema.load(payload))
            db["session"].add(vm)
            print("add")
        db["session"].commit()


# class VirtualMachine(Resource):
#     def __init__(self):
#         self.vm_schema = VirtualMachineSchema()

#     def get(self,name):
#         vm = ''
#         return vm, 200


#     def delete(self,name):
#         output = ''
#         return output
