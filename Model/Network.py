from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate
from sqlalchemy.orm import relationship

from databases.db import Base


class NetworkSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    status = fields.Str()


class Network(Base):
    __tablename__ = "Network"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    status = Column(Integer)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)
    # relationship
    interface = relationship("Interface", backref="Network", lazy=True)

    def __init__(self, name=None, status=0):
        self.name = name
        self.status = status

    def __repr__(self):
        return f"<Network {self.name}>"
