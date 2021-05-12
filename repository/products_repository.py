from typing import List, Dict, Tuple, Any, Optional, Iterable

from sqlalchemy.sql.functions import max as max_, min as min_
from sqlalchemy.sql import func
from sqlalchemy import Float

from . import db, Product, Tag, TagToProduct, ProductType, ProductPicture, Feedback


def get_all_tags() -> List[Tag]:
    return db.session.query(Tag).all()


def get_types() -> List[ProductType]:
    return db.session.query(ProductType).all()


def get_type_by_id(product_type_id: str) -> ProductType:
    return db.session.query(ProductType).filter(ProductType.id == product_type_id).first()


def get_product_by_id(product_id: str) -> Optional[Tuple[Product, Optional[int]]]:
    result = db.session.query(Product, func.avg(Feedback.stars.cast(Float)).label('average_stars')).outerjoin(Feedback).\
        filter(Product.id == product_id).group_by(Product.id).group_by(Feedback.id).first()
    if not result:
        return None
    product, stars_avg = result
    return product, stars_avg


def get_type_stat(type_id: str) -> Optional[Dict[str, Any]]:
    result = db.session.query(
        ProductType.name, min_(Product.price), max_(Product.price), min_(Feedback.stars), max_(Feedback.stars)
    ).\
        filter(ProductType.id == type_id).\
        filter(Product.type == type_id).\
        filter(Feedback.product_id == Product.id).\
        group_by(ProductType.name).first()
    if not result:
        return None
    name, min_price, max_price, min_stars, max_stars = result
    return {
        "name": name,
        "min_price": min_price,
        "max_price": max_price,
        "min_stars": min_stars,
        "max_stars": max_stars
    }


def get_products_by_type(
        type_id: str, tags: Iterable[str] = None,
        min_price: int = None, max_price: int = None,
        min_stars: int = None, max_stars: int = None
) -> List[Tuple[Product, ProductPicture, Optional[int]]]:
    query = db.session.query(Product, ProductPicture, func.avg(Feedback.stars.cast(Float)).label('average_stars')).\
        distinct(Product.id).outerjoin(Feedback).\
        filter(Product.type == type_id).\
        filter(ProductPicture.product_id == Product.id)
    if tags:
        query = query.filter(TagToProduct.tag_id.in_(tags)).filter(Product.id.in_(TagToProduct.product_id))
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if min_stars:
        query = query.filter(Feedback.stars >= min_stars)
    if max_stars:
        query = query.filter(Feedback.stars <= max_stars)
    return query.group_by(Product.id, ProductPicture.id).all()
