from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func

from Model.Users import UserModel, UserSchema
from databases.db import db


class Users(Resource):
    def __init__(self):
        self.user_schema = UserSchema()
        self.user_schema_many = UserSchema(many=True)

    def get(self):
        users = UserModel.query.all()
        result = self.user_schema_many.dump(users)

        return result, 200

    def post(self):
        payload = request.get_json()
        error = self.user_schema.validate(payload)
        if error:
            return error, 422

        user = UserModel(**self.user_schema.load(payload))
        db["session"].add(user)
        db["session"].commit()

        return self.user_schema.dump(user), 200


class User(Resource):
    def __init__(self):
        self.user_schema = UserSchema()

    def post(self, id):
        body = request.get_json()
        error = UserSchema().validate(body)
        if error:
            return error, 422

        user = UserModel.query.where(UserModel.id == id).update(
            dict(**UserSchema().load(body), updatedAt=func.now())
        )

        db["session"].commit()

        return user, 200
