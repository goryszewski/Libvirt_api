from sqlalchemy import Column, Integer, String, DateTime , ForeignKey
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base


# id: 1
# vmid: 1
# MAC: 00:00:00:00:00:00 # 17
# ip: 100.100.100.100 # 27


class IPSchema(Schema):
    id = fields.Int()
    vmid = fields.Int()
    networkid = fields.Int()
    mac = fields.Str(required=True)
    ip = fields.Str(required=True)
    mask = fields.Int(required=True)

class IP(Base):
    __tablename__ = "ip"

    id = Column(Integer, primary_key=True)
    vmid = Column(Integer,ForeignKey('VirtualMachine.id'))
    networkid = Column(Integer,ForeignKey('Network.id'))
    mask = Column(Integer)
    mac = Column(String(17))
    ip = Column(String(27))

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, vmid=None, ip=None,mask=None, mac=None):
        self.mac = mac
        self.vmid = vmid
        self.ip = ip
        self.mask = mask

    def __repr__(self):
        return f"<IP {self.ip}>"
