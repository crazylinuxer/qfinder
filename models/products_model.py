from flask_restx import fields, Namespace

from . import ModelCreator, create_id_field


api = Namespace("products", "Endpoints related to products")


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


class FeedbackShortModel(ModelCreator):
    body = fields.String(
        required=True,
        description='Text of the comment',
        example='Good product, I can recommend it!',
        min_length=2,
        max_length=4096
    )
    stars = fields.Integer(
        required=True,
        description='Number of stars left by user',
        example=4,
        min=0,
        max=5
    )


class FeedbackModel(FeedbackShortModel):
    user_name = first_name = fields.String(
        required=True,
        description='User`s name',
        example='Ivan Ivanov',
        min_length=5,
        max_length=130
    )


feedback = api.model(
    'feedback_model',
    FeedbackModel()
)


class ProductModel(ProductNamePriceModel):
    description = fields.String(
        required=True,
        description='Product description',
        example='Very good processor',
        min_length=0,
        max_length=2048
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
    feedback = fields.List(
        fields.Nested(
            feedback,
            required=True
        )
    )
    stars_avg = fields.Float(
        required=False,
        description='Average number of stars left by users',
        example=4.5,
        min=0,
        max=5
    )


class TagModel(ModelCreator):
    id = create_id_field(
        required=True,
        description="Tag ID in database"
    )
    title = fields.String(
        required=True,
        description='Tag name',
        example='High performance',
        min_length=2,
        max_length=48
    )


class TypeStatisticsModel(ModelCreator):
    id = ProductTypeModel.id
    name = ProductTypeModel.name
    min_price = fields.Integer(
        required=True,
        description="Minimum price of a product of this type",
        example=256,
        min=1,
    )
    max_price = fields.Integer(
        required=True,
        description="Maximum price of a product of this type",
        example=256,
        min=1,
    )
    min_stars = fields.Integer(
        required=True,
        description='Minimum number of stars left by user for products of this type',
        example=4,
        min=0,
        max=5
    )
    max_stars = fields.Integer(
        required=True,
        description='Maximum number of stars left by user for products of this type',
        example=4,
        min=0,
        max=5
    )


tag = api.model(
    'tag_model',
    TagModel()
)

product = api.model(
    'product_model',
    ProductModel()
)

product_id = api.model(
    'product_id_model',
    ProductIdModel()
)

type_statistics = api.model(
    'type_statistics_model',
    TypeStatisticsModel()
)
