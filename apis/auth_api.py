from flask_restx.namespace import Namespace
from flask_restx.reqparse import RequestParser
from flask_restx import fields
from flask import request, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from werkzeug.datastructures import FileStorage

from services import get_page, get_uuid
from models.auth_model import AuthModel, TokenModel
from .utils import OptionsResource


api = Namespace("auth", "User authentication and logout")


auth = api.model(
    'auth_model',
    AuthModel(),
)

token = api.model(
    'token_model',
    TokenModel()
)


@api.route('')
class Auth(OptionsResource):
    @api.doc('auth_user')
    @api.marshal_with(token, code=200)
    @api.expect(auth, validate=True)
    @api.response(401, description="Invalid credentials")
    def post(self):
        """Log into an account"""
        return None, 200


@api.route('/logout')
class LogOut(OptionsResource):
    @api.doc('logout_user')
    @api.response(200, description="Logout successful")
    @jwt_required()
    def post(self):
        """Logout from the account"""
        response = redirect("/")
        unset_jwt_cookies(response)
        return response, 200
