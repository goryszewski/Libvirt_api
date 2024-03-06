from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request

from sqlalchemy.sql import null, func

from lib.Libvirt import Libvirt
from Model.Loadbalancers import LoadbalancerModel, LoadbalancerSchema
from databases.db import db
from lib.logging import logging

class Node(Resource):
    def __init__(self):
        self.conn = Libvirt()

    def post(self):
        logging.info(request.get_json())
        content_type = request.headers.get("Content-Type")
        # body = {"function": None}
        # if content_type == "application/json":
        body = request.get_json()
        logging.info(body)

        if body["function"] == "GetNodeByHostname":
            self.conn.get()
            for vm in self.conn.get():
                if vm["hostname"] == body["hostname"]:
                    return {
                        "name": vm["hostname"],
                        "ip": {
                            "private": vm["net"]["ens3"]["addrs"][0]["addr"],
                            "public": vm["net"]["ens4"]["addrs"][0]["addr"],
                        },
                        "type": vm["OSType"],
                    }

        return {}, 404

    def get(self):
        return {"test": "GET:Node"}, 200


class Lb(Resource):
    @jwt_required()
    def __init__(self):
        self.loadbalancer_schema = LoadbalancerSchema()

    def post(self, ip=None):
        content_type = request.headers.get("Content-Type")
        body = {"function": None}

        if content_type == "application/json":
            body = request.get_json()
        print(body)
        if body["function"] == "BindLB":
            service_name = body["service"]
            ip = body["ip"]
            loadbalancer = LoadbalancerModel.query.where(
                LoadbalancerModel.ip == ip
            ).update(dict(service_name=service_name, updatedAt=func.now()))

            db["session"].commit()
            loadbalancer = LoadbalancerModel.query.where(
                LoadbalancerModel.ip == ip
            ).one()
            return self.loadbalancer_schema.dump(loadbalancer), 200

        if body["function"] == "UnBindLB":
            service_name = body["service"]
            loadbalancer = LoadbalancerModel.query.where(
                LoadbalancerModel.service_name == service_name
            ).update(dict(service_name=null(), updatedAt=func.now()))
            db["session"].commit()

            return {}, 200
        if body["function"] == "GetFirstFreeLB":
            loadbalancer = LoadbalancerModel.query.filter(
                LoadbalancerModel.service_name == null()
            ).first()
            result = self.loadbalancer_schema.dump(loadbalancer)
            return result, 200

        return {"test": "POST:LB", "json": body}, 404

    # @jwt_required()
    def get(self, ip):
        loadbalancer = LoadbalancerModel.query.where(LoadbalancerModel.ip == ip).one()
        result = self.loadbalancer_schema.dump(loadbalancer)
        return result, 200
