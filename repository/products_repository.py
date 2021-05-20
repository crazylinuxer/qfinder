from typing import List, Dict, Tuple, Any, Optional, Iterable, Set, Union

from sqlalchemy.sql.functions import count, max as max_, min as min_
from sqlalchemy.dialects.postgresql import json, array
from sqlalchemy.sql.operators import or_
from sqlalchemy.sql import func
from sqlalchemy import Float

from . import db, Product, Tag, TagToProduct, ProductType, ProductPicture, Feedback


def get_all_tags() -> List[Tag]:
    return db.session.query(Tag).all()


def get_types() -> List[ProductType]:
    return db.session.query(ProductType).all()


def get_type_by_id(product_type_id: str) -> ProductType:
    return db.session.query(ProductType).filter(ProductType.id == product_type_id).first()


def get_product_object(product_id: str) -> Product:
    return db.session.query(Product).filter(Product.id == product_id).first()


def get_full_product_by_id(product_id: str) -> Optional[Tuple[Product, List[Feedback]]]:
    feedback = db.session.query(Feedback).filter(Feedback.product_id == product_id).all()
    product = db.session.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    return product, (feedback or [])


def get_type_stat(type_id: str) -> Optional[Dict[str, Any]]:
    result = db.session.query(
        ProductType.name, min_(Product.price), max_(Product.price),
        min_(Feedback.stars), max_(Feedback.stars)
    ).\
        outerjoin(Product, Product.type == ProductType.id).outerjoin(Feedback).\
        filter(ProductType.id == type_id).group_by(ProductType.name).first()
    if not result:
        return None
    name, min_price, max_price, min_stars, max_stars = result

    all_characteristics = db.session.query(Product.characteristics).filter(Product.type == type_id).all()
    products_count = len(all_characteristics)
    characteristics_stat: Dict[str, Union[Set[str], List[str]]] = {}
    for characteristics in all_characteristics:
        for characteristic in characteristics[0]:
            if characteristic not in characteristics_stat:
                characteristics_stat[characteristic] = set()
            characteristics_stat[characteristic].add(characteristics[0][characteristic])
    for characteristic_type in list(characteristics_stat.keys()):
        characteristics_stat[characteristic_type] = list(characteristics_stat[characteristic_type])

    has_products_without_comments = (len(
        db.session.query(count(Product.id)).distinct(Product.id).
        filter(Product.type == type_id).filter(Feedback.product_id == Product.id).group_by(Product.id).all()
    ) != products_count)

    return {
        "id": type_id,
        "name": name,
        "min_price": min_price,
        "max_price": max_price,
        "min_stars": 0 if has_products_without_comments else min_stars,
        "max_stars": max_stars,
        "characteristics": characteristics_stat
    }


def get_products_by_type(
        type_id: str, tags: Iterable[str] = None,
        min_price: int = None, max_price: int = None,
        min_stars: int = None, max_stars: int = None,
        characteristics: Dict[str, Any] = None
) -> List[Tuple[Product, ProductPicture, Optional[int]]]:
    avg_stars_subquery = db.session.query(Product.id, func.avg(Feedback.stars.cast(Float)).label('average_stars')).\
        filter(Product.type == type_id).\
        filter(Feedback.product_id == Product.id).\
        group_by(Product.id).subquery()

    query = db.session.query(Product, ProductPicture, func.avg(Feedback.stars.cast(Float)).label('avg_stars')).\
        distinct(Product.id).\
        outerjoin(avg_stars_subquery, avg_stars_subquery.c.id == Product.id).\
        outerjoin(Feedback).outerjoin(ProductPicture).\
        filter(Product.type == type_id)
    if tags:
        query = query.filter(TagToProduct.tag_id.in_(tags)).filter(Product.id == TagToProduct.product_id)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if min_stars:
        query = query.filter(avg_stars_subquery.c.average_stars >= min_stars)
    if max_stars:
        query = query.filter(or_(avg_stars_subquery.c.average_stars <= max_stars, Feedback.id == None))
    if characteristics:
        for characteristic in characteristics:
            query = query.\
                filter(json.HAS_KEY(Product.characteristics, characteristic)).\
                filter(json.HAS_ANY(Product.characteristics[characteristic], array(characteristics[characteristic])))
    return query.group_by(Product.id, ProductPicture.id).all()
