from flask_restful import Resource
from flask import request
from sqlalchemy.sql import null, func


from Model.Loadbalancers import LoadbalancerModel, LoadbalancerSchema
from databases.db import db


class Loadbalancer(Resource):
    def __init__(self):
        self.loadbalancer_schema = LoadbalancerSchema()
        # self.loadbalancer_schema_many = LoadbalancerSchema(many=True)

    def get(self, id=None):
        loadbalancer = LoadbalancerModel.query.where(LoadbalancerModel.id == id).one()
        result = self.loadbalancer_schema.dump(loadbalancer)
        return result, 200

    def post(self, id=None):
        if id != None:
            return "ID not expcted", 501

        payload = request.get_json()
        logging.info(payload)

        # DOTO - get free ip , bind payload , return lb object

        return payload, 202

