from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base


class HddSchema(Schema):
    id = fields.Int()
    vmid = fields.Int()
    size = fields.Int()


class HDD(Base):
    __tablename__ = "hdd"

    id = Column(Integer, primary_key=True)
    vmid = Column(Integer,ForeignKey('VirtualMachine.id'))
    size = Column(Integer)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, vmid=None,  size=0):
        self.vmid = vmid

        self.size = size

    def __repr__(self):
        return f"<HDD {self.id}>"
