from mongoengine import (
    Document,
    StringField,
    EmbeddedDocument,
    IntField,
    ListField,
    EmbeddedDocumentField,
)
from marshmallow import Schema, fields


class Port(EmbeddedDocument):
    name = StringField()
    protocol = StringField()
    port = IntField()
    nodeport = IntField()


class Node(EmbeddedDocument):
    name = StringField()
    ip = StringField()


class LoadBalacnerModel(Document):
    ip = StringField()
    name = StringField()
    namespace = StringField()
    ports = ListField(EmbeddedDocumentField(Port))
    nodes = ListField(EmbeddedDocumentField(Node))


class PortSchema(Schema):
    name = fields.Str()
    protocol = fields.Str()
    port = fields.Int()
    nodeport = fields.Int()


class NodeSchema(Schema):
    name = fields.Str()
    ip = fields.Str()


class LoadBalacnerSchema(Schema):
    name = fields.Str()
    namespace = fields.Str()
    ports = fields.List(fields.Nested(PortSchema))
    nodes = fields.List(fields.Nested(NodeSchema))
