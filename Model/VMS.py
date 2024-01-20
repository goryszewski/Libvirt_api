from marshmallow import Schema, fields, validate

class VMSchema(Schema):
    id = fields.Int()
    memory = fields.Int(required=True)
    cpu = fields.Int(required=True)
    name = fields.Str(required=True)
