from flask_restful import Resource
from flask import request

from lib.Libvirt import Libvirt
from lib.logging import logging
from Model.VMS import NodeSshSchema


class V2_Node(Resource):
    def __init__(self):
        self.conn = Libvirt()

    def get(self, name: str = None):
        if name:
            vm = self.conn.getVmByName(name)

            if not vm:
                return {}, 404

            return vm.ToJson(), 200

        vms = self.conn.GetVms()
        output = []
        for vm in vms:
            output.append(vm.ToJson())
        return output, 200

class V2_Node_SSH(Resource):
    def __init__(self):
        self.conn = Libvirt()
        self.node_ssh_schema = NodeSshSchema()

    def post(self,name):
        vm = self.conn.getVmByName(name)
        payload = request.get_json()

        error = self.node_ssh_schema.validate(payload)
        if error:
            print(error)
            return error, 422

        vm.setSSH(payload['user'],payload['key'])

        return {},204


class V2_NodeBindDisk(Resource):
    def __init__(self):
        self.conn = Libvirt()

    def get(self, name: str, hdd_id: str = None):
        vm = self.conn.getVmByName(name)

        if hdd_id:
            device = vm.getDiskByPath(path=f"/var/lib/libvirt/images/{hdd_id}.qcow2")

            if device:
                output = device.address
                return output, 200
        else:
            return vm.getDisksJson(), 200
        return {}, 404

    def put(self, name: str, hdd_id: str = None):
        if not hdd_id:
            return {}, 501
        vm = self.conn.getVmByName(name)
        disk = vm.AttachDisk(hdd_id)
        if not disk:
            return {}, 404
        return disk.ToJson(), 200

    def delete(self, name: str, hdd_id: str = None):
        if not hdd_id:
            return {}, 501
        vm = self.conn.getVmByName(name)
        isOk = vm.DetachDisk(hdd_id)
        if not isOk:
            return {}, 404
        return {}, 200
