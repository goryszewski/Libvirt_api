from mongoengine import (
    Document,
    StringField,
)

from marshmallow import Schema, fields


class Account(Document):
    email = StringField()


class Account(Schema):
    email = fields.Str()
