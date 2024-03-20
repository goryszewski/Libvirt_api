from mongoengine import (
    Document,
    StringField,
    EmbeddedDocument,
    IntField,
    ListField,
    EmbeddedDocumentField,
)
from marshmallow import Schema, fields


class Ports(EmbeddedDocument):
    name = StringField()
    protocol = StringField()
    port = IntField()
    nodeport = IntField()


class LoadBalacnerModel(Document):
    ip = StringField()
    name = StringField()
    namespace = StringField()
    ports = ListField(EmbeddedDocumentField(Ports))


class PortSchema(Schema):
    name = fields.Str()
    protocol = fields.Str()
    port = fields.Int()
    nodeport = fields.Int()


class LoadBalacnerSchema(Schema):
    ip = fields.Str()
    name = fields.Str()
    namespace = fields.Str()
    ports = fields.List(fields.Nested(PortSchema))
