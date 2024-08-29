from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    DictField,
    EnumField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    ObjectIdField,
)

from enum import Enum
from bson import ObjectId
from marshmallow import Schema, fields

# Account


class StatusAccount(Enum):
    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"
    DEACTIVATED = "deactivated"
    EXPIRED = "expired"
    REVOKED = "revoked"


class StatusOrder(Enum):
    PENDING = "pending"
    VALID = "valid"


class JWKSchema(Schema):
    kty = fields.Str()  # RSA
    e = fields.Str()  # "AQAB",
    n = (
        fields.Str()
    )  # "kelRgJ24OdzXSWtiTemBG39ZD8pMwCeXlkq8kp-6qVsNzcxpR9ieGq6Bo9KMLajYO4Pzr4XKN47vfGmLSZ6kvUy4NVrbcWCtaywEXMyr6EiFzQF5R0tROMMD1vHmiBQq3w0H1vl_1ln-GQLmUrp9nJ9wPXy_N8ver1-4gd1l5KH2CIE6NThBsLQsU2nADV22-I7I1Dg25hiixvHSElDFtRH2wSPmZDlG86JJS7zb3raqaVR-oi7xVoK-5cFzSIPyj2U2bbjlq9Q6KwavaPGDyPgj6WLbhpaNFhg63TU7kHJQWNWB3huL7Lon8lTOLvVDhFa4C_XI-PJdbJPajIDWHxasSBy1ux88NXMNsbTVbNFANXPEJffq0zRqOgW6Fzu8_ImiD_oI33I76OLAhW9sYnExrArOQVy3UVlQuoYHyhkUVRYICoki_pIO9O4yzTNqHb6qIHYFAsMsEeGqcEaaLjS7VDZlyimgAtztlLbaZggGh544GYMI0NfXimDqVwlZHfE_ZsI881qyMqEY1UUK8JB9-sb7U7viw4dr_OBasbxOG-kEZTK4vHs6cmmERJigzKFhoX-02IMoEDweyBI-eVqe5l11kJaOVOcBmL9bSvGVyxkSAiNZUr5ioDbrnIrPOW-5oI1EyhBFQMaP9kPiwmPZkJnK-tQfOUSlUesRbYE"


class AccountProtectSchema(Schema):
    alg = fields.Str()  # RS256
    jwk = fields.Nested(JWKSchema)
    nonce = fields.Str()  # "6S8dQIvS7eL2ls4K2fB2sz-9I23cZJq_iBYjGn4Z7H8",
    url = fields.Str()  # "http://10.17.3.1:8050/acme/new-account"}


class AccountPayloadSchema(Schema):
    contact = fields.List(fields.Str())
    jwk = fields.Str()
    termsOfServiceAgreed = fields.Bool()
    onlyReturnExisting = fields.Bool()


class IdentifierSchema(Schema):
    type = fields.Str()
    value = fields.Str()


class RequestOrderSchema(Schema):
    identifiers = fields.List(fields.Nested(IdentifierSchema))


class Identifier(EmbeddedDocument):
    type = StringField()
    value = StringField()


class ChallengeModel(EmbeddedDocument):
    id = ObjectIdField(required=True, default=lambda: ObjectId())
    url = StringField()
    type = StringField()
    status = StringField()
    token = StringField()
    validation = StringField()


class AuthorizationModel(EmbeddedDocument):
    id = ObjectIdField(required=True, default=lambda: ObjectId())
    status = StringField()
    expires = StringField()
    identifier = DictField()
    challenges = ListField(EmbeddedDocumentField(ChallengeModel))
    wildcard = BooleanField()


class OrderModel(EmbeddedDocument):
    id = StringField()
    status = EnumField(StatusOrder, default=StatusOrder.PENDING)
    expires = StringField()
    identifiers = ListField(EmbeddedDocumentField(Identifier))
    notBefore = StringField()
    notAfter = StringField()
    error = DictField()
    authorizations = ListField(EmbeddedDocumentField(AuthorizationModel))
    finalize = StringField()
    certificate = StringField()


class AccountModel(Document):
    contact = ListField(StringField())
    jwk = StringField()
    termsOfServiceAgreed = BooleanField()
    orders = ListField(EmbeddedDocumentField(OrderModel))
    status = EnumField(StatusAccount, default=StatusAccount.VALID)


# Cert


class CertModel(Document):
    orderid = StringField()
    cert = StringField()
