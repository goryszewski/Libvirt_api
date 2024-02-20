from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func


from Model.Hdds import HddSchema, HDD
from databases.db import db


class HddR(Resource):
    def __init__(self):
        self.hdd_schema = HddSchema()

    def get(self, vmid):
        hdd = HDD.query.where(HDD.vmid == vmid).all()
        result = self.hdd_schema.dump(hdd)
        return result, 200
