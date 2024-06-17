import subprocess
from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func


from Model.Hdds import HddSchema, Hdd
from databases.db import db
from lib.logging import logging


class BindHddResource(Resource):
    def __init__(self):
        pass

    def get(self, hdd_id,vm_id):
        cmd=["virsh","attach-disk","--domain",vm_id,f"/var/lib/libvirt/images/{hdd_id}.qcow2","--target","vdb","--persistent"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)

        if (result.returncode != 0):
            return {"ERROR":result.returncode },501

        result ={
            "test":"ok",
            "hdd_id":hdd_id,
            "vm_id":vm_id
                 }
        statuscode = 201
        return result, statuscode

    def delete(self, hdd_id,vm_id):
        cmd = ["virsh","detach-disk","--domain",vm_id,f"/var/lib/libvirt/images/{hdd_id}.qcow2","--persistent"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)

        if (result.returncode != 0):
            return {"ERROR":result.returncode },501

        result ={
            "test":"ok",
            "hdd_id":hdd_id,
            "vm_id":vm_id
                 }
        statuscode = 202
        return result, statuscode


## TODO live add
# virsh attach-disk --domain vmname /var/lib/libvirt/images/vmname-vdb.qcow2 --target vdb --persistent --config --live
# virsh detach-disk --domain vmname /var/lib/libvirt/images/vmname-vdb.qcow2 --persistent --config --live
