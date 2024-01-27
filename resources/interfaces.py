from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func


from Model.Interfaces import InterfaceSchema,InterfaceModel
from databases.db import db

class Interface(Resource):
    def __init__(self):
        self.interface_schema = InterfaceSchema()
    def get(self,vmid):
        interface = InterfaceModel.query.where(InterfaceModel.vmid == vmid).all()
        result = self.interface_schema.dump(interface)
        return result, 200
