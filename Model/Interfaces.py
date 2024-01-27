from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base


class InterfaceSchema(Schema):
    id = fields.Int()
    vmid = fields.Int()
    name = fields.Str(required=True)
    ip = fields.Str(required=True)


class InterfaceModel(Base):
    __tablename__ = "Interface"

    id = Column(Integer, primary_key=True)
    vmid = Column(Integer)
    name = Column(String(50))
    ip = Column(String(50))

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, vmid=None, ip=None, name=None):
        self.name = name
        self.vmid = vmid
        self.ip = ip


    def __repr__(self):
        return f"<Interface {self.name}>"
