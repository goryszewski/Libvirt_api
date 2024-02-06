from flask_restful import Resource
from flask import request
from sqlalchemy.sql import null,func


from Model.Loadbalancers import LoadbalancerModel, LoadbalancerSchema
from databases.db import db


class Loadbalancer(Resource):
    def __init__(self):
        self.loadbalancer_schema = LoadbalancerSchema()
        # self.loadbalancer_schema_many = LoadbalancerSchema(many=True)

    def get(self,id):
        loadbalancer = LoadbalancerModel.query.where(LoadbalancerModel.id == id).one()
        result = self.loadbalancer_schema.dump(loadbalancer)
        return result, 200

    def post(self,id):
        service_name = request.args.get('service_name')
        if not service_name:
            service_name = null()
        loadbalancer = LoadbalancerModel.query.where(LoadbalancerModel.id == id).update(dict(service_name=service_name,updatedAt=func.now()))

        db["session"].commit()
        loadbalancer = loadbalancer = LoadbalancerModel.query.where(LoadbalancerModel.id == id).one()
        return self.loadbalancer_schema.dump(loadbalancer),202





class Loadbalancers(Resource):
    def __init__(self):
        self.loadbalancer_schema = LoadbalancerSchema()
        self.loadbalancer_schema_many = LoadbalancerSchema(many=True)

    def get(self):
        type_output = request.args.get('filter')

        if type_output == '3':
            loadbalancer = LoadbalancerModel.query.where(LoadbalancerModel.service_name == null()).all()
        elif type_output == '2':
            loadbalancer = LoadbalancerModel.query.filter(LoadbalancerModel.service_name == null()).first()
            result = self.loadbalancer_schema.dump(loadbalancer)
            return result, 200
        else:
            loadbalancer = LoadbalancerModel.query.all()

        result = self.loadbalancer_schema_many.dump(loadbalancer)
        return result, 200
