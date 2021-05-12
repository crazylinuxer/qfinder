from flask_jwt_extended import get_jwt_identity, jwt_required, create_refresh_token, create_access_token

from services import user_service
from models.user_model import api, auth, account_model, account_edit_model, sign_up, token
from utils import OptionsResource


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
    @api.marshal_with(token, code=200)
    @api.response(401, description="Invalid credentials")
    @api.response(404, description="User not found")
    def post(self):
        """Log into an account"""
        return user_service.auth_user(**api.payload)


@api.route('/auth/refresh')
class AuthRefresh(OptionsResource):
    @api.doc('employee_auth_refresh', security='apikey')
    @api.marshal_with(token, code=200)
    @jwt_required(refresh=True)
    def post(self):
        """Refresh pair of tokens"""
        identity = get_jwt_identity()
        return {
               'access_token': create_access_token(identity=identity),
               'refresh_token': create_refresh_token(identity=identity),
               'user_id': identity
        }, 200


@api.route('')
class Account(OptionsResource):
    @api.doc('get_account', security='apikey')
    @jwt_required()
    @api.marshal_with(account_model, code=200)
    def get(self):
        """Get the account info"""
        return user_service.get_user_account(get_jwt_identity()), 200

    @api.doc('edit_account', security='apikey')
    @jwt_required()
    @api.marshal_with(account_model, code=200)
    @api.expect(account_edit_model, validate=True)
    def put(self):
        """Edit the account info"""
        return user_service.edit_user_account(get_jwt_identity(), **api.payload), 200
