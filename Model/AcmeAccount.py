from mongoengine import Document, StringField, ListField, BooleanField

from marshmallow import Schema, fields


class AccountModel(Document):
    contact = ListField(StringField())
    termsOfServiceAgreed = BooleanField()


class AccountSchema(Schema):
    contact = fields.List(fields.Str())
    termsOfServiceAgreed = fields.Bool()
