from flask_jwt_extended import get_jwt_identity

from models.goods_model import api, product, short_product, product_type, product_id, cart
from models import required_query_params
from utils import uses_jwt, OptionsResource


@api.route('/types')
class ProductTypes(OptionsResource):
    @api.doc('get_product_types')
    @api.marshal_with(product_type, as_list=True, code=200)
    def get(self):
        """Get all product types"""
        return None, 200


@api.route('/by_type')
class ProductsByType(OptionsResource):
    @api.doc('get_products_by_type', params=required_query_params({"type": "ID of the type"}))
    @api.response(404, description="Type not found")
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


@api.route('/cart')
class Cart(OptionsResource):
    @api.doc('get_cart')
    @uses_jwt()
    @api.marshal_with(cart, code=200)
    def get(self):
        """Get user's cart content"""
        return None, 200

    @api.doc('add_to_cart')
    @uses_jwt()
    @api.expect(product_id, validate=True)
    @api.response(404, description="Product not found")
    @api.response(200, description="Success")
    def post(self):
        """Add an item to the user's cart"""
        return None, 200

    @api.doc('remove_from_cart', params={"product": "ID of the product to remove"})
    @uses_jwt()
    @api.response(404, description="Product not found")
    @api.response(409, description="Product not in the cart")
    @api.response(200, description="Success")
    def delete(self):
        """Remove an item from the user's cart.
        Cart will be cleared if the 'product' parameter is null"""
        return None, 200


@api.route('/wishlist')
class Wishlist(OptionsResource):
    @api.doc('get_wishlist')
    @uses_jwt()
    @api.marshal_with(short_product, as_list=True, code=200)
    def get(self):
        """Get user's wishlist content"""
        return None, 200

    @api.doc('add_to_wishlist')
    @uses_jwt()
    @api.expect(product_id, validate=True)
    @api.response(404, description="Product not found")
    @api.response(200, description="Success")
    def post(self):
        """Add an item to the user's wishlist"""
        return None, 200

    @api.doc('remove_from_wishlist', params=required_query_params({"product": "ID of the product to remove"}))
    @uses_jwt()
    @api.response(404, description="Product not found")
    @api.response(409, description="Product not in the wishlist")
    @api.response(200, description="Success")
    def delete(self):
        """Remove an item from the user's wishlist"""
        return None, 200

