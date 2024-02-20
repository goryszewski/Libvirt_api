from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func


from Model.Ips import IPSchema,IP
from databases.db import db


class Interface(Resource):
    def __init__(self):
        self.interface_schema = IPSchema()

    def get(self, vmid):
        interface =IP.query.where(IP.vmid == vmid).all()
        result = self.interface_schema.dump(interface)
        return result, 200
