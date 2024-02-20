from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base


# id: 1
# vm_id: 1
# MAC: 00:00:00:00:00:00 # 17
# ip: 100.100.100.100 # 27


class InterfaceSchema(Schema):
    id = fields.Int()
    vm_id = fields.Int()
    network_id = fields.Int()

    mac = fields.Str(required=True)
    ip = fields.Str(required=True)
    mask = fields.Int(required=True)


class Interface(Base):
    __tablename__ = "Interface"

    id = Column(Integer, primary_key=True)
    vm_id = Column(Integer, ForeignKey("VirtualMachine.id"))
    network_id = Column(Integer, ForeignKey("Network.id"))

    mask = Column(Integer)
    mac = Column(String(17))
    ip = Column(String(27))

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, vm_id=None, ip=None, mask=None, mac=None, network_id=None):
        self.mac = mac
        self.vm_id = vm_id
        self.ip = ip
        self.mask = mask
        self.network_id = network_id

    def __repr__(self):
        return f"<Interface {self.ip}>"
