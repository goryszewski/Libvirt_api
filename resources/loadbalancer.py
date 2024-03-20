from flask_restful import Resource
from flask import request

import json

from Model.Mongo_LB import LoadBalacnerModel, LoadBalacnerSchema


class Loadbalancer(Resource):
    def __init__(self):
        self.loadbalancer_schema = LoadBalacnerSchema()

    def get(self, id=None):
        all = LoadBalacnerModel.objects

        return json.loads(all.to_json())

    def post(self, id=None):
        payload = request.get_json()
        error = self.loadbalancer_schema.validate(payload)
        if error:
            return error, 422

        lb = LoadBalacnerModel(**self.loadbalancer_schema.dump(payload))
        lb.save()

        return json.loads(lb.to_json()), 200

    def put(self, id=None):
        payload = request.get_json()
        error = self.loadbalancer_schema.validate(payload)
        if error:
            return error, 422

        lb = LoadBalacnerModel.objects(
            name=payload["name"], namespace=payload["namespace"]
        ).first()
        if not lb:
            return {}, 404

        lb.update(**payload)
        lb = LoadBalacnerModel.objects(
            name=payload["name"], namespace=payload["namespace"]
        ).first()

        return json.loads(lb.to_json()), 200

    def delete(self, id=None):
        payload = request.get_json()
        error = self.loadbalancer_schema.validate(payload)
        if error:
            return error, 422

        lb = LoadBalacnerModel.objects(
            name=payload["name"], namespace=payload["namespace"]
        )
        if not lb:
            return {}, 404

        lb.delete()
        return {}, 202
