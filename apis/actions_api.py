from flask_jwt_extended import get_jwt_identity, jwt_required

from services import actions_service
from models.actions_model import actions_short_product, cart, feedback_action, api
from models import required_query_params
from models.products_model import product_id
from utils import OptionsResource, get_uuid


@api.route('/cart')
class Cart(OptionsResource):
    @api.doc('get_cart', security='apikey')
    @jwt_required()
    @api.marshal_with(cart, code=200)
    def get(self):
        """Get user's cart content"""
        return actions_service.get_cart_content(get_jwt_identity()), 200

    @api.doc('add_to_cart', security='apikey')
    @jwt_required()
    @api.expect(product_id, validate=True)
    @api.response(404, description="Product not found")
    @api.response(409, description="Product is already in the cart")
    @api.response(201, description="Success")
    def post(self):
        """Add an item to the user's cart"""
        return actions_service.add_to_cart(get_jwt_identity(), api.payload.get("id")), 201

    @api.doc('remove_from_cart', security='apikey', params={"product_id": "ID of the product to remove"})
    @jwt_required()
    @api.response(404, description="Product not found")
    @api.response(409, description="Product not in the cart")
    @api.response(200, description="Success")
    def delete(self):
        """Remove an item from the user's cart.
        Cart will be cleared if the 'product' parameter is null"""
        return actions_service.remove_from_cart(get_jwt_identity(), get_uuid("product_id")), 200


@api.route('/wishlist')
class Wishlist(OptionsResource):
    @api.doc('get_wishlist', security='apikey')
    @jwt_required()
    @api.marshal_with(actions_short_product, as_list=True, code=200)
    def get(self):
        """Get user's wishlist content"""
        return actions_service.get_wishlist_content(get_jwt_identity()), 200

    @api.doc('add_to_wishlist', security='apikey')
    @jwt_required()
    @api.expect(product_id, validate=True)
    @api.response(404, description="Product not found")
    @api.response(409, description="Product is already in the wishlist")
    @api.response(201, description="Success")
    def post(self):
        """Add an item to the user's wishlist"""
        return actions_service.add_to_wishlist(get_jwt_identity(), api.payload.get("id")), 201

    @api.doc('remove_from_wishlist', security='apikey',
             params=required_query_params({"product_id": "ID of the product to remove"}))
    @jwt_required()
    @api.response(404, description="Product not found")
    @api.response(409, description="Product not in the wishlist")
    @api.response(200, description="Success")
    def delete(self):
        """Remove an item from the user's wishlist"""
        return actions_service.remove_from_wishlist(get_jwt_identity(), get_uuid("product_id")), 200


@api.route('/feedback')
class Feedback(OptionsResource):
    @api.doc('add_feedback', security='apikey')
    @jwt_required()
    @api.expect(feedback_action, validate=True)
    @api.response(404, description="Product not found")
    @api.response(201, description="Success")
    def post(self):
        """Add a feedback to the product"""
        print(api.payload)
        return actions_service.leave_feedback(get_jwt_identity(), **api.payload), 201

    @api.doc('remove_feedback', security='apikey',
             params=required_query_params({"feedback_id": "ID of the feedback to remove"}))
    @jwt_required()
    @api.response(404, description="Feedback not found")
    @api.response(403, description="Can not remove this feedback (does not belong to user)")
    @api.response(200, description="Success")
    def delete(self):
        """Remove a feedback"""
        return actions_service.remove_feedback(get_jwt_identity(), get_uuid("feedback_id")), 200
