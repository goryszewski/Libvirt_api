from flask_restful import Resource
from flask import request

import json

from Model.Mongo_LB import LoadBalacnerModel, LoadBalacnerSchema


class Loadbalancer(Resource):
    def __init__(self):
        self.loadbalancer_schema = LoadBalacnerSchema()

    def _findFreeIp(self):
        network = "10.10.10"
        items = LoadBalacnerModel.objects()
        for item in items:
            if item.name == "" and item.namespace == "":
                return item

        return f"{network}.{len(items)+1}"

    # list all or first
    def get(self, name=None, namespace=None):
        if name and namespace:
            all = LoadBalacnerModel.objects(name=name, namespace=namespace).first()
        else:
            all = LoadBalacnerModel.objects(name__ne="", namespace__ne="")

        if not all:
            return {}, 404

        return json.loads(all.to_json())

    def post(self, name=None, namespace=None):
        payload = request.get_json()
        error = self.loadbalancer_schema.validate(payload)
        if error:
            print(error)
            return error, 422

        lb = LoadBalacnerModel.objects(
            name=payload["name"], namespace=payload["namespace"]
        )
        if lb:
            return (
                "Service: {name} exist is namespace: {namespace}".format(**payload),
                500,
            )

        ip = self._findFreeIp()

        if not isinstance(ip, str):
            ip.update(**self.loadbalancer_schema.dump(payload))
            lb = LoadBalacnerModel.objects(
                name=payload["name"], namespace=payload["namespace"]
            ).first()
            return json.loads(lb.to_json()), 200

        lb = LoadBalacnerModel(**self.loadbalancer_schema.dump(payload), ip=ip)
        lb.save()
        return json.loads(lb.to_json()), 200

    def put(self, name=None, namespace=None):
        payload = request.get_json()
        error = self.loadbalancer_schema.validate(payload)
        if error:
            return error, 422

        lb = LoadBalacnerModel.objects(
            name=payload["name"], namespace=payload["namespace"]
        ).first()
        if not lb:
            return {}, 200

        lb.update(**payload)
        lb = LoadBalacnerModel.objects(
            name=payload["name"], namespace=payload["namespace"]
        ).first()

        return json.loads(lb.to_json()), 200

    def delete(self, name=None, namespace=None):
        payload = request.get_json()
        error = self.loadbalancer_schema.validate(payload)
        if error:
            return error, 422

        lb = LoadBalacnerModel.objects(
            name=payload["name"], namespace=payload["namespace"]
        )
        if not lb:
            return {}, 200

        lb.update(name="", namespace="", ports=[], nodes=[])
        return {}, 200
