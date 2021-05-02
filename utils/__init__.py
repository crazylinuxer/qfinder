from typing import Iterable

from flask import Flask, redirect, make_response, request
from flask_restx import Namespace, Resource
from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended import (create_access_token, create_refresh_token, unset_jwt_cookies, unset_access_cookies,
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

        def remove_jwt_cookie(result):
            if isinstance(result, tuple):
                if result[0] is None:
                    result = 'null', *(result[1:])
                result = make_response(*result)
                unset_access_cookies(result)
            else:
                unset_access_cookies(result)
            return result

        def jwt_wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request(optional=True)
                without_access_token = get_jwt().get("type") != 'access'
                verify_jwt_in_request(refresh=True, optional=optional)
                without_refresh_token = get_jwt().get("type") != 'refresh'
                if without_refresh_token and not optional:
                    return remove_jwt_cookie(redirect('/'))
                result = function(*args, **kwargs)
                if without_access_token and not optional:
                    return renew_jwt_cookie(result)
                else:
                    if without_refresh_token:
                        return unset_access_cookies(result)
                    return renew_jwt_cookie(result, refresh=True)
            except ExpiredSignatureError:
                try:
                    verify_jwt_in_request(refresh=True, optional=optional)
                    identity = get_jwt_identity()
                    if not identity and not optional:
                        return remove_jwt_cookie(redirect('/'))
                    result = function(*args, **kwargs)
                    if identity:
                        return renew_jwt_cookie(result)
                    return remove_jwt_cookie(result)
                except ExpiredSignatureError:
                    result = redirect('/')
                    unset_jwt_cookies(result)
                    return result
        jwt_wrapper.__name__ = function.__name__
        jwt_wrapper.__doc__ = function.__doc__
        return jwt_wrapper
    return jwt_usage_decorator


api = Namespace("")


class OptionsResource(Resource):
    @api.hide
    def options(self):
        return None, 200
