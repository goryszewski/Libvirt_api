from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func

from Model.Network import Network,NetworkSchema
from databases.db import db

class NetworkResource(Resource):
    def __init__(self):
        self.network_schema = NetworkSchema()
        self.network_schemamany = NetworkSchema(many=True)
    def _return(self,id):
        vm = Network.query.where(Network.id == id).one()
        result = self.network_schema.dump(vm)
        return result , 200

    def get(self,id=None):
        if id:
            network = Network.query.where().all()
            result = self.network_schemamany.dump(network)
            return result, 200
        return {},404

    def post(self,id=None):
        if id != None:
            return "ID not expcted",501
        payload = request.get_json()
        error = self.network_schema.validate(payload)
        if error:
            return error, 422

        net = Network(**self.network_schema.load(payload))
        db["session"].add(net)
        db["session"].flush()
        db["session"].refresh(net)

        db["session"].commit()


        return self._return(net.id)

    def put(self,id=None):
        pass

    def delete(self,id=None):
        pass
