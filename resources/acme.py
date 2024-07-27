from flask_restful import Resource
from flask import request,jsonify

url="https://127.0.0.1:8050"

class Directory(Resource):
    def __init__(self):
        pass
    def get(self):
        output = {
            "newNonce": f"{url}/new-nonce",
            "newAccount": f"{url}/new-account",
            "newOrder": f"{url}/new-order",
            "revokeCert": f"{url}/revoke-cert",
            "keyChange": f"{url}/key-change",
        }
        return output,200
    def post(sefl):
        return "",501
    def put(self):
        return "",501

class NewAccount(Resource):
    def __init__(self):
        pass
    def get(self):
        return "",501
    def post(sefl):
        output = {
            "contact":"",
            "status":"valid",
            "orders": ""
        }

        return output,201
    def put(self):
        return "",501

class NewOrder(Resource):
    def __init__(self):
        pass
    def get(self):
        return "",501
    def post(sefl):
        return "",501
    def put(self):
        return "",501

class AcmeChallenge(Resource):
    def __init__(self):
        pass
    def get(self):
        return "",501
    def post(sefl):
        return "",501
    def put(self):
        return "",501

class Finalize(Resource):
    def __init__(self):
        pass
    def get(self):
        return "",501
    def post(sefl):
        return "",501
    def put(self):
        return "",501

class RevokeCert(Resource):
    def __init__(self):
        pass
    def get(self):
        return "",501
    def post(sefl):
        return "",501
    def put(self):
        return "",501
