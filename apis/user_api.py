from flask_restx.namespace import Namespace
from flask import redirect
from flask_jwt_extended import unset_refresh_cookies, set_refresh_cookies, get_jwt_identity

from services import user_service
from models.user_model import AuthModel, SignUpModel, AccountModel, AccountEditModel
from utils import uses_jwt, OptionsResource

api = Namespace("user", "User account actions")


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


@api.route('/signup')
class SignUp(OptionsResource):
    @api.doc('sign_up')
    @api.response(201, "Success")
    @api.response(422, "Incorrect password given")
    @api.response(409, "Username or email exists")
    @api.expect(sign_up, validate=True)
    def post(self):
        """Create an account"""
        user_service.register_user(**api.payload)
        return None, 201


@api.route('/auth')
class Auth(OptionsResource):
    @api.doc('auth_user')
    @api.expect(auth, validate=True)
    @api.response(200, description="Success")
    @api.response(401, description="Invalid credentials")
    @api.response(404, description="User not found")
    def post(self):
        """Log into an account"""
        response = redirect("/")
        access_token, refresh_token = user_service.auth_user(**api.payload)
        set_refresh_cookies(response, refresh_token)
        return response


@api.route('/logout')
class LogOut(OptionsResource):
    @api.doc('logout_user')
    @uses_jwt(optional=True)
    @api.response(200, description="Logout successful")
    def post(self):
        """Logout from the account"""
        response = redirect("/")
        unset_refresh_cookies(response)
        return response


@api.route('')
class Account(OptionsResource):
    @api.doc('get_account')
    @uses_jwt()
    @api.marshal_with(account_model, code=200)
    def get(self):
        """Get the account info"""
        return user_service.get_user_account(get_jwt_identity()), 200

    @api.doc('edit_account')
    @uses_jwt()
    @api.marshal_with(account_model, code=200)
    @api.expect(account_edit_model, validate=True)
    def put(self):
        """Edit the account info"""
        return user_service.edit_user_account(get_jwt_identity(), **api.payload), 200
