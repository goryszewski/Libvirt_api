from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func

from Model.Network import Network, NetworkSchema
from Model.Interfaces import Interface
from databases.db import db
from lib.logging import logging


class NetworkResource(Resource):
    def __init__(self):
        self.schema = NetworkSchema()
        self.schemaM = NetworkSchema(many=True)

    def _return(self, id):
        net = Network.query.where(Network.id == id).one()
        result = self.schema.dump(net)
        print(result)
        return result, 200

    def get(self, id=None):
        network = []
        statuscode = 200
        if id:
            network = Network.query.where(Network.id == id, Network.status != 2).all()

            # result = self.schemaM.dump(network)
            # return result, 200
        else:
            network = Network.query.where(Network.status != 2).all()
        result = self.schemaM.dump(network)

        if network == []:
            statuscode = 404

        return result, statuscode

    def post(self, id=None):
        logging.info(request.get_json())
        if id != None:
            return "ID not expcted", 501
        payload = request.get_json()
        error = self.schema.validate(payload)
        if error:
            return error, 422

        net = Network(**self.schema.load(payload))
        db["session"].add(net)
        db["session"].flush()
        db["session"].refresh(net)

        db["session"].commit()

        return self._return(net.id)

    def put(self, id=None):
        return {}, 501

    def delete(self, id):
        update_payload = dict(status=2, updatedAt=func.now())
        interface = Interface.query.where(Interface.network_id == id).all()
        if interface:
            return "resource used", 501
        network = Network.query.where(Network.id == id).update(update_payload)
        db["session"].commit()
        return network, 200
