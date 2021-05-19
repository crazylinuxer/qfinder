import json

from flask import request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.products_model import api, product, product_type, tag, type_statistics
from models.actions_model import short_product
from models import required_query_params, query_param_to_set
from utils import OptionsResource, get_uuid
from services import products_service


@api.route('/types')
class ProductTypes(OptionsResource):
    @api.doc('get_product_types')
    @api.marshal_with(product_type, as_list=True, code=200)
    def get(self):
        """Get all product types"""
        return products_service.get_product_types(), 200


@api.route('/tags')
class ProductTags(OptionsResource):
    @api.doc('get_product_tags')
    @api.marshal_with(tag, as_list=True, code=200)
    def get(self):
        """Get all tags"""
        return products_service.get_tags(), 200


@api.route('/type_stat')
class ProductTypeStat(OptionsResource):
    @api.doc('get_product_type_stat', params=required_query_params({"type": "ID of the type"}))
    @api.marshal_with(type_statistics, code=200)
    @api.response(404, description="Type not found")
    def get(self):
        """Get statistics of the given type such as min/max stars and min/max price"""
        return products_service.get_product_type_stat(get_uuid("type")), 200


@api.route('/by_type')
class ProductsByType(OptionsResource):
    @api.doc('get_products_by_type', params={
        **required_query_params({"type": "ID of the type"}),
        "tags": "Tag IDs to include (all products will be included if this param is empty), separated by commas",
        "min_price": {"type": int, "description": "Minimal price to show"},
        "max_price": {"type": int, "description": "Maximal price to show"},
        "min_stars": {"type": float, "description": "Minimum stars to show"},
        "max_stars": {"type": float, "description": "Maximum stars to show"},
        "characteristics": {
            "type": str, "description": "Product characteristics to include (for example, '{\"Frequency\":\"4 GHz\"}')"
        }
    })
    @api.response(404, description="Type or tag not found")
    @api.marshal_with(short_product, as_list=True, code=200)
    def get(self):
        """Get all products of given type"""
        characteristics_raw = request.args.get("characteristics")
        characteristics = None
        if characteristics_raw:
            try:
                characteristics = json.loads(characteristics_raw)
            except (ValueError, TypeError):
                abort(400, "Incorrect characteristics parameter")
        return products_service.get_products_by_type(
            get_uuid("type"),
            query_param_to_set("tags"),
            request.args.get("min_price"),
            request.args.get("max_price"),
            request.args.get("min_stars"),
            request.args.get("max_stars"),
            characteristics
        ), 200


@api.route('/info')
class ProductInfo(OptionsResource):
    @api.doc('get_product_info', security='apikey', params=required_query_params({"product": "ID of the product"}))
    @api.response(404, description="Product not found")
    @api.marshal_with(product, code=200)
    @jwt_required(optional=True)
    def get(self):
        """Get product info"""
        return products_service.get_product_info(get_jwt_identity(), get_uuid("product")), 200
