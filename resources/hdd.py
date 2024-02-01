from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func


from Model.Hdds import HddSchema, HddModel
from databases.db import db


class Hdd(Resource):
    def __init__(self):
        self.hdd_schema = HddSchema()

    def get(self, vmid):
        hdd = HddModel.query.where(HddModel.vmid == vmid).all()
        result = self.hdd_schema.dump(hdd)
        return result, 200
