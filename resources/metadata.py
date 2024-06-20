from flask_restful import Resource
from flask import request
from lib.Libvirt import Libvirt


class V2_Metadata(Resource):
    def __init__(self):
        self.conn = Libvirt()

    def get(self):
        # self.conn.getVmByIp()

        return request.remote_addr
