from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, validate

from databases.db import Base
from .Interfaces import InterfaceSchema
from .Hdds import HddSchema

# 0 - todo create
# 1 - created
# 2 - deleted
# 3 - todo delete


class VirtualMachineSchema(Schema):
    id = fields.Int()
    memory = fields.Int(required=True)
    cpu = fields.Int(required=True)
    name = fields.Str(required=True)
    status = fields.Int()
    disk = fields.List(fields.Nested(HddSchema))
    interface = fields.List(fields.Nested(InterfaceSchema))


class VirtualMachine(Base):
    __tablename__ = "VirtualMachine"

    id = Column(Integer, primary_key=True)
    memory = Column(Integer)
    cpu = Column(Integer)
    name = Column(String(50))
    status = Column(String(50))
    interface = relationship("Interface", backref="VirtualMachine", lazy=True)
    disk = relationship("Hdd", backref="VirtualMachine", lazy=True)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, memory=None, cpu=None, name=None, status=0):
        self.name = name
        self.memory = memory
        self.cpu = cpu
        self.status = status

    def __repr__(self):
        return f"<VirtualMachine {self.name}>"
