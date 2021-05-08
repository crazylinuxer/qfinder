from models.goods_model import api, product, product_type, tag
from models.actions_model import goods_short_product
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


@api.route('/by_type')
class ProductsByType(OptionsResource):
    @api.doc('get_products_by_type', params={
        **required_query_params({"type": "ID of the type"}),
        **{"tags": "Tag IDs to include (all products will be included if this param is empty), separated by commas"}
    })
    @api.response(404, description="Type or tag not found")
    @api.marshal_with(goods_short_product, as_list=True, code=200)
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