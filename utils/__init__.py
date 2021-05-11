from typing import Iterable
from uuid import UUID

from flask import Flask, make_response, jsonify, request, abort
from flask_restx import Namespace, Resource
from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask_jwt_extended import (create_access_token, create_refresh_token, unset_access_cookies,
                                get_jwt_identity, set_access_cookies, verify_jwt_in_request,
                                set_refresh_cookies, get_jwt)


def get_current_app() -> Flask:
    from server import app
    return app


def any_non_nones(iterable: Iterable) -> bool:
    for i in iterable:
        if i is not None:
            return True
    return False


def uses_jwt(optional=False):
    """
    This should be used on top of Namespace.marshal_with
    """
    def jwt_usage_decorator(function):
        def renew_jwt_cookie(result, refresh=False):
            token = (create_refresh_token if refresh else create_access_token)(identity=get_jwt_identity())
            if isinstance(result, tuple):
                if result[0] is None:
                    result = 'null', *(result[1:])
                result = make_response(*result)
            else:
                result = make_response(result)
            (set_refresh_cookies if refresh else set_access_cookies)(result, token)
            return result

        def remove_jwt_cookie(result, unset_func):
            if isinstance(result, tuple):
                if result[0] is None:
                    result = 'null', *(result[1:])
                result = make_response(*result)
                unset_func(result)
            else:
                unset_func(result)
            return result

        def jwt_wrapper(*args, **kwargs):
            access_token_data = refresh_token_data = None
            try:
                verify_jwt_in_request(optional=optional)
                access_token_data = get_jwt()
            except (ExpiredSignatureError, NoAuthorizationError, InvalidHeaderError):
                pass
            try:
                verify_jwt_in_request(optional=optional, refresh=True)
                refresh_token_data = get_jwt()
            except (ExpiredSignatureError, NoAuthorizationError, InvalidHeaderError):
                pass
            if not refresh_token_data:
                if optional:
                    return remove_jwt_cookie(function(*args, **kwargs), unset_access_cookies)
                return remove_jwt_cookie(make_response(jsonify(message="Invalid token"), 401), unset_access_cookies)
            if not access_token_data:
                return renew_jwt_cookie(function(*args, **kwargs))
            return renew_jwt_cookie(function(*args, **kwargs), refresh=True)

        jwt_wrapper.__name__ = function.__name__
        jwt_wrapper.__doc__ = function.__doc__
        jwt_wrapper.__apidoc__ = function.__apidoc__
        return jwt_wrapper
    return jwt_usage_decorator


api = Namespace("")


class OptionsResource(Resource):
    @api.hide
    def options(self):
        return None, 200


def get_uuid(param_name, allow_empty: bool = False) -> str:
    if isinstance(request, str):
        value = request
    else:
        value = request.args.get(param_name, '')
    if not value and allow_empty:
        return value
    try:
        UUID(value)
    except ValueError:
        abort(400, f"Incorrect '{param_name}' parameter (must match UUID v4)")
    except TypeError:
        abort(400, f"Cannot find '{param_name}' parameter of correct type (must appear once in query)")
    return value
