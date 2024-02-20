from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, validate

from databases.db import Base


class VirtualMachineSchema(Schema):
    id = fields.Int()
    memory = fields.Int(required=True)
    cpu = fields.Int(required=True)
    name = fields.Str(required=True)
    status = fields.Int()
    # 0 - todo create
    # 1 - created
    # 2 - deleted

class HddSchema(Schema):
    id = fields.Int()
    size = fields.Int(required=True)

class IPSchema(Schema):
    id = fields.Int()
    ip = fields.Str(required=True)
    mask = fields.Int(required=True)
    mac = fields.Str(required=True)

class NewVirtualMachineSchema(Schema):
    id = fields.Int()
    memory = fields.Int(required=True)
    cpu = fields.Int(required=True)
    name = fields.Str(required=True)
    disk = fields.List(fields.Nested(HddSchema))
    ip = fields.List(fields.Nested(IPSchema))



class VirtualMachineModel(Base):
    __tablename__ = "VirtualMachine"

    id = Column(Integer, primary_key=True)
    memory = Column(Integer)
    cpu = Column(Integer)
    name = Column(String(50))
    status = Column(String(50))
    ip = relationship('IP', backref='VirtualMachine', lazy=True)
    disk = relationship('HDD', backref='VirtualMachine', lazy=True)


    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, memory=None, cpu=None, name=None, status=0):
        self.name = name
        self.memory = memory
        self.cpu = cpu
        self.status = status

    def __repr__(self):
        return f"<VirtualMachine {self.name}>"
