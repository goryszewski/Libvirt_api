from flask_restful import Resource
from flask import Response, request
from flask_jwt_extended import create_access_token
from marshmallow import Schema, fields
import datetime
from lib.logging import logging


class AUTHSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class LoginApi(Resource):
    def __init__(self):
        self.auth_schema = AUTHSchema()

    def get(self):
        return "Use POST Method", 401

    def post(self):
        logging.info(request.get_json())
        body = request.get_json()

        error = AUTHSchema().validate(body)
        if error:
            return error, 422

        if body["username"] != body["password"]:
            return "Wrong username or password", 401

        expires = datetime.timedelta(days=1)
        token = create_access_token(body["username"], expires_delta=expires)
        return {"token": token}, 200
