from flask_restful import Resource
from flask import request
from sqlalchemy.sql import func

from Model.Tasks import TaskModel,TaskSchema
from databases.db import db

class Tasks(Resource):
    def __init__(self):
        self.task_schema = TaskSchema()
        self.task_schema_many = TaskSchema(many=True)

    def get(self):
        tasks = TaskModel.query.all()
        result = self.task_schema_many.dump(tasks)

        return result, 200

    def post(self):
        payload= request.get_json()
        error = self.task_schema.validate(payload)
        if error:
            return error, 422

        task = TaskModel(**self.task_schema.load(payload))
        db["session"].add(task)
        db["session"].commit()

        return self.task_schema.dump(task), 200

class Task(Resource):
    def __init__(self):
        self.task_schema = TaskSchema()

    def post(self,id):
        body = request.get_json()
        error = TaskSchema().validate(body)
        if error:
            return error,422

        task = TaskModel.query.where(TaskModel.id==id).update(
            dict(**TaskSchema().load(body), updatedAt=func.now())
        )

        db["session"].commit()

        return task,200
