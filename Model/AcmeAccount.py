from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    DictField,
    EmbeddedDocumentField,
    EmbeddedDocument,
)

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


class Identifier(EmbeddedDocument):
    type = StringField()
    value = StringField()


class OrderModel(Document):
    status = StringField()
    expires = StringField()
    identifiers = ListField(EmbeddedDocumentField(Identifier))
    notBefore = StringField()
    notAfter = StringField()
    error = DictField()
    authorizations = fields.List(fields.Str())
    finalize = StringField()
    certificate = StringField()


class IdentifierSchema(Schema):
    type = fields.Str()
    value = fields.Str()


class RequestOrderSchema(Schema):
    identifiers = fields.List(fields.Nested(IdentifierSchema))


# Authorization


class ChallengeModel(EmbeddedDocument):
    url = StringField()
    type = StringField()
    status = StringField()
    token = StringField()
    validated = StringField()


class AuthorizationModel(Document):
    orderid = StringField()
    status = StringField()
    expires = StringField()
    identifier = DictField()
    challenges = ListField(DictField())
    wildcard = BooleanField()


# Cert


class CertModel(Document):
    orderid = StringField()
    cert = StringField()
