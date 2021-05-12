from typing import List, Dict, Tuple, Any, Optional, Iterable

from sqlalchemy.sql.functions import sum, count
from flask_sqlalchemy import BaseQuery

from . import db, Product, Tag, TagToProduct, ProductType, Feedback


def get_all_tags() -> List[Tag]:
    return db.session.query(Tag).all()


def get_types() -> List[ProductType]:
    return db.session.query(ProductType).all()


def get_product_by_id(product_id: str) -> Tuple[Product, Optional[int]]:
    product, stars_count, stars_sum = db.session.query(Product, count(Feedback.stars), sum(Feedback.stars)).\
        filter(Product.id == product_id).filter(Feedback.product_id == product_id).first()
    return product, (stars_sum / stars_count if stars_count else None)


def get_stars_query(base: BaseQuery) -> BaseQuery:
    pass


def get_type_stat(type_id: str) -> Dict[str, Any]:
    pass


def get_products_by_type(
        type_id: str, tags: Iterable[str] = None,
        min_price: int = None, max_price: int = None,
        min_stars: int = None, max_stars: int = None
) -> List[Tuple[Product, Optional[int]]]:
    query = db.session.query(Product).filter(Product.type == type_id)
    if tags:
        query = query.filter(TagToProduct.tag_id.in_(tags)).filter(Product.id.in_(TagToProduct.product_id))
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if min_stars:
        query = query.filter()  # todo stars
    if max_stars:
        query = query.filter()  # todo stars
    return query.all()
