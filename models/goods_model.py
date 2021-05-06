from flask_restx import fields, Namespace

from . import ModelCreator, create_id_field


api = Namespace("goods", "Endpoints related to products")


class ProductIdModel(ModelCreator):
    id = create_id_field(
        required=True,
        description="Product ID in database"
    )


class PictureModel(ModelCreator):
    link = fields.String(
        required=True,
        description="Link to the picture",
        example="http://www.amd.com/system/files/11157-ryzen-5-pib-left-facing-1260x709.png",
        min_length=7,
        max_length=1024
    )


picture = api.model(
    'picture_model',
    PictureModel()
)


class ProductTypeModel(PictureModel):
    id = create_id_field(
        required=True,
        description="Product type ID in database"
    )
    name = fields.String(
        required=True,
        description='Product type name',
        example='Processors',
        min_length=2,
        max_length=64
    )


product_type = api.model(
    'product_type_model',
    ProductTypeModel()
)


class ProductNamePriceModel(ProductIdModel):
    name = fields.String(
        required=True,
        description='Product name',
        example='AMD Ryzen 5 1600X',
        min_length=2,
        max_length=128
    )
    price = fields.Integer(
        required=True,
        description="Price of a product",
        example=256,
        min=1,
    )


class ShortProductModel(ProductNamePriceModel):
    picture = PictureModel.link


short_product = api.model(
    'short_product_model',
    ShortProductModel()
)


class ProductModel(ProductNamePriceModel):
    description = fields.String(
        required=True,
        description='Product description',
        example='Very good processor',
        min_length=0,
        max_length=1024
    )
    characteristics = fields.Raw(
        {},
        required=True,
        description="Product characteristics"
    )
    type = fields.Nested(
        product_type,
        required=True
    )
    pictures = fields.List(
        fields.Nested(
            picture,
            required=True
        )
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


product = api.model(
    'product_model',
    ProductModel()
)

product_id = api.model(
    'product_id_model',
    ProductIdModel()
)

cart = api.model(
    'cart_model',
    CartModel()
)
