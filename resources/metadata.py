from flask_restful import Resource
from flask import request
from lib.Libvirt import Libvirt


class V2_Metadata(Resource):
    def __init__(self):
        self.conn = Libvirt()

    def get(self):
        vm = self.conn.getVmByIp(request.remote_addr)

        return vm
