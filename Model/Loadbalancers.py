from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base


class ServiceLBSchema(Schema):
    id = fields.Int()
    lb_id = fields.Int()
    port = fields.Int()
    lb_port = fields.Int()


class LoadbalancerSchema(Schema):
    id = fields.Int()
    ip = fields.Str(required=True)
    name = fields.Str(required=True)
    namespace = fields.Str(required=True)


class NodeSchema(Schema):
    id = fields.Int()
    lb_id = fields.Int()
    name = fields.Str(required=True)
    namespace = fields.Str(required=True)


class LoadbalancerModel(Base):
    __tablename__ = "Loadbalancer"

    id = Column(Integer, primary_key=True)
    ip = Column(String(50))
    service_name = Column(String(50))

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, ip=None, service_name=1):
        self.ip = ip
        self.service_name = service_name

    def __repr__(self):
        return f"<Loadbalancer {self.ip}>"
