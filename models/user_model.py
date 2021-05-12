from flask_restx import fields, Namespace

from . import create_email_field, ModelCreator, PASSWORD_EXAMPLE, create_id_field


api = Namespace("user", "User account actions")


class UserIdModel(ModelCreator):
    id = create_id_field(
        required=True,
        description="User`s ID in database"
    )


class EmailModel(ModelCreator):
    email = create_email_field(
        required=True,
        description="User`s email (login)"
    )


class PasswordModel(ModelCreator):
    password = fields.String(
        required=True,
        description='User`s password',
        example=PASSWORD_EXAMPLE,
        min_length=8,
        max_length=64
    )


class NameModel(ModelCreator):
    first_name = fields.String(
        required=False,
        description='User`s first name',
        example='Ivan',
        min_length=2,
        max_length=64
    )
    last_name = fields.String(
        required=False,
        description='User`s last name',
        example='Ivanov',
        min_length=2,
        max_length=64
    )


class AuthModel(PasswordModel, EmailModel):
    pass


class SignUpModel(PasswordModel, EmailModel, NameModel):
    pass


class AccountEditModel(EmailModel, NameModel):
    pass


class AccountModel(EmailModel, NameModel, UserIdModel):
    pass


class TokenModel(UserIdModel):
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


token = api.model(
    'token_model',
    TokenModel()
)

auth = api.model(
    'auth_model',
    AuthModel(),
)

sign_up = api.model(
    'sign_up_model',
    SignUpModel()
)

account_model = api.model(
    'account_model',
    AccountModel()
)

account_edit_model = api.model(
    'account_edit_model',
    AccountEditModel()
)
