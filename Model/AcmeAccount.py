from mongoengine import Document, StringField, ListField, BooleanField, DictField

from marshmallow import Schema, fields

# Account


class AccountModel(Document):
    contact = ListField(StringField())
    termsOfServiceAgreed = BooleanField()
    orders = StringField()
    status = StringField()


class AccountSchema(Schema):
    contact = fields.List(fields.Str())
    termsOfServiceAgreed = fields.Bool()
    # orders = fields.Str()
    # status = fields.Str()


# Order


class OrderModel(Document):
    status = StringField()
    expires = StringField()
    identifiers = ListField(DictField())
    notBefore = StringField()
    notAfter = StringField()
    error = DictField()
    authorizations = fields.List(fields.Str())
    finalize = StringField()
    certificate = StringField()
