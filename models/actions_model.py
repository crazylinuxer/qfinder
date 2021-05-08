from flask_restx import fields, Namespace

from models import ModelCreator
from models.goods_model import ProductNamePriceModel, PictureModel, ProductModel, FeedbackShortModel, api as goods_api


api = Namespace("actions", "Actions of user")


class ShortProductModel(ProductNamePriceModel):
    picture = PictureModel.link


short_product = api.model(
    'short_product_model',
    ShortProductModel()
)


goods_short_product = goods_api.model(
    'goods_short_product_model',
    ShortProductModel()
)


class CartModel(ModelCreator):
    content = fields.List(
        fields.Nested(
            short_product,
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
