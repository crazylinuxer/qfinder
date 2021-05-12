from typing import List, Dict, Set, Any

from repository import products_repository, Tag


def get_product_type_stat(type_id: str, **_) -> Dict[str, Any]:
    return products_repository.get_type_stat(type_id)


def get_products_by_type(
        product_type: str, tags: Set[str] = None,
        min_price: int = None, max_price: int = None,
        min_stars: int = None, max_stars: int = None, **_
) -> List[Dict[str, Any]]:
    products = products_repository.get_products_by_type(product_type, tags, min_price, max_price, min_stars, max_stars)
    return [{**product[0].as_dict, "stars_avg": product[1], "type": product[0].type_ref} for product in products]


def get_product_info(product_id: str, **_) -> Dict[str, Any]:
    product, stars = products_repository.get_product_by_id(product_id)
    return {**product.as_dict, "stars_avg": stars, "type": product.type_ref}


def get_tags(**_) -> List[Tag]:
    return products_repository.get_all_tags()


def get_product_types(**_) -> List[Dict[str, str]]:
    return [{**product_type.as_dict, "link": product_type.picture} for product_type in products_repository.get_types()]
