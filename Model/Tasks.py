from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base

# class JobSchema


class TaskSchema(Schema):
    id = fields.Int()
    payload = fields.Str(required=True)
    status = fields.Int(required=True)


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True)
    payload = Column(String(50))
    status = Column(Integer)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, payload=None, status=1):
        self.payload = payload
        self.status = status

    def __repr__(self):
        return f"<Task {self.name}>"
