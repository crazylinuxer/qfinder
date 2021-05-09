from flask_jwt_extended import get_jwt_identity

from models.actions_model import actions_short_product, cart, feedback_action, api
from models import required_query_params
from models.products_model import product_id
from utils import uses_jwt, OptionsResource


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
    @api.marshal_with(actions_short_product, as_list=True, code=200)
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


@api.route('/feedback')
class Feedback(OptionsResource):
    @api.doc('add_feedback')
    @uses_jwt()
    @api.expect(feedback_action, validate=True)
    @api.response(404, description="Product not found")
    @api.response(200, description="Success")
    def post(self):
        """Add a feedback to the product"""
        return None, 200

    @api.doc('remove_feedback', params=required_query_params({"feedback_id": "ID of the feedback to remove"}))
    @uses_jwt()
    @api.response(404, description="Feedback not found")
    @api.response(403, description="Can not remove this feedback (does not belong to user)")
    @api.response(200, description="Success")
    def delete(self):
        """Remove a feedback"""
        return None, 200
