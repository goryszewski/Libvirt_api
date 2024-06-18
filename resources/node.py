from flask_restful import Resource
from flask import request

from lib.Libvirt import Libvirt
from lib.logging import logging


class V2_Node(Resource):
    def __init__(self):
        self.conn = Libvirt()

    def get(self, name: str = None):
        if name:
            vm = self.conn.getVmByName(name)
            return vm.ToJson(), 200

        vms = self.conn.GetVms()
        output = []
        for vm in vms:
            output.append(vm.ToJson())
        return output, 200


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
        isOk = vm.AttachDisk(hdd_id)
        if not isOk:
            return {}, 404
        return {}, 200

    def delete(self, name: str, hdd_id: str = None):
        if not hdd_id:
            return {}, 501
        vm = self.conn.getVmByName(name)
        isOk = vm.DetachDisk(hdd_id)
        if not isOk:
            return {}, 404
        return {}, 200
