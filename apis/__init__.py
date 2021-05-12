from flask import Blueprint, current_app
from flask_restx import Api

from .user_api import api as auth_api
from .products_api import api as products_api
from .actions_api import api as actions_api


api_bp = Blueprint('api', __name__)

authorization = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


class CustomApi(Api):
    def handle_error(self, e):
        for val in current_app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e
        return super().handle_error(e)


api = CustomApi(
    api_bp,
    title='QFinder API',
    version='0.0.1-dev',
    doc='/',
    description='API documentation for the QualityFinder',
    authorizations=authorization
)


api.namespaces.clear()
api.add_namespace(auth_api)
api.add_namespace(products_api)
api.add_namespace(actions_api)


cors_headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Methods": "*"
}
