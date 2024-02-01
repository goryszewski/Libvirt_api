from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base


class HddSchema(Schema):
    id = fields.Int()
    vmid = fields.Int()
    name = fields.Str()
    path = fields.Str()
    size = fields.Int()


class HddModel(Base):
    __tablename__ = "hdd"

    id = Column(Integer, primary_key=True)
    vmid = Column(Integer)
    name = Column(String(255))
    path = Column(String(255))
    size = Column(Integer)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, vmid=None, name=None, path=None, size=0):
        self.vmid = vmid
        self.name = name
        self.path = path
        self.size = size

    def __repr__(self):
        return f"<hdd {self.name}>"
