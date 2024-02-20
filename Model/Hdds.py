from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base


class HddSchema(Schema):
    id = fields.Int()
    vm_id = fields.Int()
    size = fields.Int()


class Hdd(Base):
    __tablename__ = "Hdd"

    id = Column(Integer, primary_key=True)
    vm_id = Column(Integer, ForeignKey("VirtualMachine.id"))
    size = Column(Integer)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, vm_id=None, size=0):
        self.vm_id = vm_id

        self.size = size

    def __repr__(self):
        return f"<HDD {self.id}>"
