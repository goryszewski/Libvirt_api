from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func


from Model.Interfaces import InterfaceSchema, Interface
from databases.db import db


class InterfaceResource(Resource):
    def __init__(self):
        self.schema = InterfaceSchema()

    def get(self, vm_id):
        interface = Interface.query.where(Interface.vm_id == vm_id).all()
        result = self.schema.dump(interface)
        return result, 200
