from flask_restx.namespace import Namespace
from flask_restx.reqparse import RequestParser
from flask_restx import fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage

from services import get_page, get_uuid
from models.auth_model import AuthModel, TokenModel
from .utils import OptionsResource


api = Namespace("attachment", "Attachments for news posts")


auth = api.model(
    'auth_model',
    AuthModel(),
)

token = api.model(
    'token_model',
    TokenModel()
)


@api.route('/')
class Auth(OptionsResource):
    @api.doc('employee_auth')
    @api.marshal_with(token, code=200)
    @api.expect(auth, validate=True)
    @api.response(401, description="Invalid credentials")
    def post(self):
        """Log into an account"""
        return auth_service.get_token(**api.payload), 200
