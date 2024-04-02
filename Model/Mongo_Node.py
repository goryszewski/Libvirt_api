from mongoengine import (
    Document,
    StringField,
    EmbeddedDocument,
    IntField,
    ListField,
    EmbeddedDocumentField,
)
from marshmallow import Schema, fields


class DiskModel(Document):
    name = StringField()
    path = StringField()
    size = StringField()


class NetworkModel(Document):
    name = StringField()
    mac = StringField()
    ip = StringField()


class NodeModel(Document):
    name = StringField()
    disks = ListField(EmbeddedDocumentField(DiskModel))
    networks = ListField(EmbeddedDocumentField(NetworkModel))
