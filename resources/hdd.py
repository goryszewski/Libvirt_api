from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func


from Model.Hdds import HddSchema, Hdd
from databases.db import db


class HddResource(Resource):
    def __init__(self):
        self.schema = HddSchema()
        self.schemaM = HddSchema(many=True)

    def get(self, vm_id):
        hdd = Hdd.query.where(Hdd.vm_id == vm_id).all()
        result = self.schema.dump(hdd)
        return result, 200
