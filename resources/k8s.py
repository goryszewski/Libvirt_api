from flask_restful import Resource
from flask import request


from lib.Libvirt import Libvirt
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
                        "internal": vm["net"]["ens3"]["addrs"][0]["addr"],
                        "external": vm["net"]["ens4"]["addrs"][0]["addr"],
                        "type": vm["OSType"],
                    }

        return {}, 404

    def get(self):
        return {"test": "GET:Node"}, 200
