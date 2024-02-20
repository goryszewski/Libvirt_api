from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func

from Model.Hdds import HDD, HddSchema
from Model.Ips import IP, IPSchema
from Model.VMS import VirtualMachineSchema, VirtualMachineModel , NewVirtualMachineSchema
from Model.Tasks import TaskModel, TaskSchema
from databases.db import db


from lib.Libvirt import Libvirt
from lib.logging import logging

import logging

class Cloud(Resource):
    def __init__(self):
        self.conn = Libvirt()

    def get(self):
        result = {"workers": []}

        self.conn.get()
        for vm in self.conn.get():
            node = {
                "name": vm["hostname"],
                "ip": {
                    "private": vm["net"]["ens3"]["addrs"][0]["addr"],
                    "public": vm["net"]["ens4"]["addrs"][0]["addr"],
                },
                "type": vm["OSType"],
            }
            logging.info(node)

            result["workers"].append(node)

        return result, 200

class VirtualMachine(Resource):
    def __init__(self):
        self.vm_schema = VirtualMachineSchema()
        self.vm_schema_many = VirtualMachineSchema(many=True)
        self.new_vm_schema = NewVirtualMachineSchema()
        self.new_vm_schema_many = NewVirtualMachineSchema(many=True)
        self.task_schema = TaskSchema()
        self.conn = Libvirt()

    def _return(self,id):
        vm = VirtualMachineModel.query.where(VirtualMachineModel.id == id).one()
        result = self.vm_schema.dump(vm)
        return result , 200


    def get(self, id=None):
        if id != None:
            vm = VirtualMachineModel.query.where(VirtualMachineModel.id == id).all()
            print(vm)
            if not vm:
                return {}, 404
            result = self.new_vm_schema_many.dump(vm)[0]
            return result, 200
        vm = VirtualMachineModel.query.where(VirtualMachineModel.status != 2).all()
        result = self.new_vm_schema_many.dump(vm)
        return result, 200

    def put(self,id=None):
        if id == None:
            return "ID expcted",500
        payload = request.get_json()
        vm = VirtualMachineModel.query.where(VirtualMachineModel.id == id).all()
        if vm:
            vm = VirtualMachineModel.query.where(VirtualMachineModel.id == id).update(dict(**VirtualMachineSchema().load(payload), updatedAt=func.now()))
            db["session"].commit()
            return self._return(id)
        else:
            return {},404


    def post(self,id=None):
        if id != None:
            return "ID not expcted",501
        payload = request.get_json()
        error = self.new_vm_schema.validate(payload)
        if error:
            return error, 422

        disks = payload.pop('disk')
        ips = payload.pop('ip')

        vm = VirtualMachineModel(**self.vm_schema.load(payload))
        db["session"].add(vm)
        db["session"].flush()
        db["session"].refresh(vm)

        #disks['vmid']=vm.id
        #ips['vmid']=vm.id

        for item in disks:
            # item['vmid']=vm.id
            disk = HDD(**HddSchema().load(item),vmid=vm.id)
            db["session"].add(disk)

        for item in ips:
            # item['vmid']=vm.id
            ip = IP(**IPSchema().load(item),vmid=vm.id)
            db["session"].add(ip)

        db["session"].commit()


        return self._return(vm.id)

    def delete(self, id):
        update_payload = dict(status=2,updatedAt=func.now())
        vm = VirtualMachineModel.query.where(VirtualMachineModel.id == id)
        print(vm)
        vm.update(update_payload)
        print(vm)
        db["session"].commit()
        return {},200
