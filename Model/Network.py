from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate
from sqlalchemy.orm import relationship

from databases.db import Base

class NetworkSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class Network(Base):
    __tablename__ = "network"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ip = relationship('IP', backref='Network', lazy=True)

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, name=None):
        self.name = name


    def __repr__(self):
        return f"<Network {self.name}>"
