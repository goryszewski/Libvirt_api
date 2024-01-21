from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from databases.db import Base

from marshmallow import Schema, fields, validate


class VirtualMachineSchema(Schema):
    id = fields.Int()
    memory = fields.Int(required=True)
    cpu = fields.Int(required=True)
    name = fields.Str(required=True)
    status = fields.Int()

class VirtualMachine(Base):
    __tablename__ = "VirtualMachine"

    id =Column(Integer, primary_key=True)
    memory =Column(Integer)
    cpu =Column(Integer)
    name =Column(String(50))
    status =Column(String(50))

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, memory=None, cpu=None, name=None, status=None):
        self.name = name
        self.memory = memory
        self.cpu = cpu
        self.status=status

    def __repr__(self):
        return f"<VirtualMachine {self.name}>"
