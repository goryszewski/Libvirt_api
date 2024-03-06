from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import sqlalchemy as sa
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate
from sqlalchemy.orm import relationship

from databases.db import Base


class NetworkSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    status = fields.Int()
    mode = fields.Str(validate=validate.OneOf(["NAT", "ROUTED", "OPEN","ISOLATED",""]))
    ipv4_dhcp = fields.Int()
    ipv4_network = fields.Str()
    ipv4_end = fields.Str()
    ipv4_start = fields.Str()
    dns_name = fields.Str()

class Network(Base):
    __tablename__ = "Network"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    mode = Column(String(50),nullable=True)
    status = Column(Integer,nullable=True)
    ipv4_dhcp = Column(Integer,nullable=True)
    ipv4_network = Column(String(50),nullable=True)
    ipv4_end = Column(String(50),nullable=True)
    ipv4_start = Column(String(50),nullable=True)
    dns_name = Column(String(50),nullable=True)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)
    # relationship
    interface = relationship("Interface", backref="Network", lazy=True)

    def __init__(self, name=None, status=0, mode=None, ipv4_dhcp=None, ipv4_network=None, ipv4_end=None, ipv4_start=None, dns_name=None):
        self.name = name
        self.status = status
        self.mode = mode
        self.ipv4_dhcp = ipv4_dhcp
        self.ipv4_network = ipv4_network
        self.ipv4_end = ipv4_end
        self.ipv4_start = ipv4_start
        self.dns_name = dns_name

    def __repr__(self):
        return f"<Network {self.name}>"
