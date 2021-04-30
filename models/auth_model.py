from enum import Enum

from flask_restx import fields

from . import create_id_field, create_email_field, ModelCreator, PASSWORD_EXAMPLE, copy_field


class EmployeeType(Enum):
    user = 0
    moderator = 1
    admin = 2


class EmailModel(ModelCreator):
    email = create_email_field(
        required=True,
        description="Employee`s email (login)"
    )


class EmployeeIdModel(ModelCreator):
    id = create_id_field(
        required=True,
        description="Employee`s ID in database"
    )


class PasswordModel(ModelCreator):
    password = fields.String(
        required=True,
        description='Employee`s password',
        example=PASSWORD_EXAMPLE,
        min_length=8,
        max_length=64
    )


class AuthModel(PasswordModel, EmailModel):
    pass


class TokenModel(EmployeeIdModel):
    access_token = fields.String(
        required=True,
        description='Token to access resources',
        example='qwerty'
    )
    refresh_token = fields.String(
        required=True,
        description='Token to refresh pair of tokens',
        example='qwerty'
    )
