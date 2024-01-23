from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func

from Model.VMS import VirtualMachineSchema, VirtualMachineModel
from Model.Tasks import TaskModel, TaskSchema
from databases.db import db


class VirtualMachines(Resource):
    def __init__(self):
        self.vm_schema = VirtualMachineSchema()
        self.vm_schema_many = VirtualMachineSchema(many=True)

    def get(self):
        vm = VirtualMachineModel.query.all()
        result = self.vm_schema_many.dump(vm)
        return result, 200

    def post(self):
        payload = request.get_json()
        error = self.vm_schema.validate(payload)
        if error:
            return error, 422

        vm = VirtualMachineModel.query.where(
            VirtualMachineModel.name == payload["name"]
        ).all()

        if vm:
            vm = VirtualMachineModel.query.where(
                VirtualMachineModel.name == payload["name"]
            ).update(dict(**VirtualMachineSchema().load(payload), updatedAt=func.now()))
            print("update")
        else:
            vm = VirtualMachineModel(**self.vm_schema.load(payload))
            db["session"].add(vm)
            print("add")
        db["session"].commit()


class VirtualMachine(Resource):
    def __init__(self):
        self.vm_schema = VirtualMachineSchema()
        self.vm_schema_many = VirtualMachineSchema(many=True)
        self.task_schema = TaskSchema()

    def get(self, id):
        print(id)
        vm = VirtualMachineModel.query.where(VirtualMachineModel.id == id).one()
        result = self.vm_schema.dump(vm)
        return result, 200

    def delete(self, id):
        task = TaskModel(payload=id, status=0)
        db["session"].add(task)
        db["session"].commit()
        return self.task_schema.dump(task)
