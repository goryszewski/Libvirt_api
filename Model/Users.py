from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from marshmallow import Schema, fields, validate

from databases.db import Base


class UserSchema(Schema):
    id = fields.Int()
    login = fields.Str(required=True)
    password = fields.Int()


class UserModel(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    password = Column(String(50))

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password

    def __repr__(self):
        return f"<User {self.login}>"
