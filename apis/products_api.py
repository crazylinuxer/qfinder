from models.products_model import api, product, product_type, tag, type_statistics
from models.actions_model import short_product
from models import required_query_params
from utils import OptionsResource


@api.route('/types')
class ProductTypes(OptionsResource):
    @api.doc('get_product_types')
    @api.marshal_with(product_type, as_list=True, code=200)
    def get(self):
        """Get all product types"""
        return None, 200


@api.route('/tags')
class ProductTags(OptionsResource):
    @api.doc('get_product_tags')
    @api.marshal_with(tag, as_list=True, code=200)
    def get(self):
        """Get all tags"""
        return None, 200


@api.route('/type_stat')
class ProductTypeStat(OptionsResource):
    @api.doc('get_product_type_stat', params=required_query_params({"type": "ID of the type"}))
    @api.marshal_with(type_statistics, code=200)
    @api.response(404, description="Type not found")
    def get(self):
        """Get statistics of the given type such as min/max stars and min/max price"""
        return None, 200


@api.route('/by_type')
class ProductsByType(OptionsResource):
    @api.doc('get_products_by_type', params={
        **required_query_params({"type": "ID of the type"}),
        "tags": "Tag IDs to include (all products will be included if this param is empty), separated by commas",
        "min_price": {"type": int, "description": "Minimal price to show"},
        "max_price": {"type": int, "description": "Maximal price to show"},
        "min_stars": {"type": float, "description": "Minimum stars to show"},
        "max_stars": {"type": float, "description": "Maximum stars to show"}
    })
    @api.response(404, description="Type or tag not found")
    @api.marshal_with(short_product, as_list=True, code=200)
    def get(self):
        """Get all products of given type"""
        return None, 200


@api.route('/info')
class ProductInfo(OptionsResource):
    @api.doc('get_product_info', params=required_query_params({"product": "ID of the product"}))
    @api.response(404, description="Product not found")
    @api.marshal_with(product, code=200)
    def get(self):
        """Get product info"""
        return None, 200
