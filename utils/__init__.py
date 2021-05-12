from typing import Iterable
from uuid import UUID

from flask import Flask, request, abort
from flask_restx import Namespace, Resource


def get_current_app() -> Flask:
    from server import app
    return app


def any_non_nones(iterable: Iterable) -> bool:
    for i in iterable:
        if i is not None:
            return True
    return False


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
