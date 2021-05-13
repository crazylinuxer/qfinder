from flask_restx import fields, Namespace

from models import ModelCreator
from models.products_model import ProductBaseModel, PictureModel, ProductModel, FeedbackShortModel, api as products_api


api = Namespace("actions", "Actions of user")


class ShortProductModel(ProductBaseModel):
    picture = PictureModel.link


actions_short_product = api.model(
    'actions_short_product_model',
    ShortProductModel()
)


short_product = products_api.model(
    'short_product_model',
    ShortProductModel()
)


class CartModel(ModelCreator):
    content = fields.List(
        fields.Nested(
            actions_short_product,
            required=True
        )
    )
    total_price = fields.Integer(
        required=True,
        description="Total price of a cart",
        example=256,
        min=1,
    )


cart = api.model(
    'cart_model',
    CartModel()
)


class FeedbackActionModel(FeedbackShortModel):
    product_id = ProductModel.id


feedback_action = api.model(
    'feedback_action_model',
    FeedbackActionModel()
)
