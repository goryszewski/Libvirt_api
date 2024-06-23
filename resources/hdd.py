import subprocess
from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func


from Model.Hdds import HddSchema, Hdd
from databases.db import db
from lib.logging import logging


class HddResource(Resource):
    def __init__(self):
        self.schema = HddSchema()
        self.schemaM = HddSchema(many=True)

    def _return(self, id: int):
        T = Hdd.query.where(Hdd.id == id).one()
        result = self.schema.dump(T)
        print(result)
        return result, 200

    def get(self, id:int):
        hdd = []
        statuscode = 200

        if id:
            hdd = Hdd.query.where(Hdd.id == id, Hdd.status != 2).all()
        else:
            hdd = Hdd.query.where(Hdd.status != 2).all()

        result = self.schemaM.dump(hdd)

        if hdd == []:
            statuscode = 404

        return result, statuscode

    def put(self, id: int):
        payload = request.get_json()
        error = self.schema.validate(payload)
        if error:
            return error, 422
        hdd = Hdd(**self.schema.load(payload))
        cmd = ["qemu-img","resize","-f","qcow2","-q",f"/var/lib/libvirt/images/{id}.qcow2",f"{hdd.size}G"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        print(result.stdout)
        if result.returncode == 0:
            return {},200

        return {},500
    def post(self, id:int=0):
        logging.info(request.get_json())
        if id != 0:
            return "ID not expcted", 501
        payload = request.get_json()
        error = self.schema.validate(payload)
        if error:
            return error, 422

        hdd = Hdd(**self.schema.load(payload))
        db["session"].add(hdd)
        db["session"].flush()
        db["session"].refresh(hdd)

        db["session"].commit()

        cmd = ["qemu-img","create","-f","qcow2",f"/var/lib/libvirt/images/{hdd.id}.qcow2",f"{hdd.size}G"]

        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        if result.returncode == 0:
            return self._return(hdd.id)

        return {},500

    def delete(self, id:int):
        update_payload = dict(status=2, updatedAt=func.now())
        hdd = Hdd.query.where(Hdd.id == id).update(update_payload)
        db["session"].commit()

        cmd = ["rm","-rf",f"/var/lib/libvirt/images/{id}.qcow2"]

        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        if result.returncode == 0:
            return {},200

        return {},500
