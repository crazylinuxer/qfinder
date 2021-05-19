from typing import List, Dict, Set, Any

from flask import abort

from repository import products_repository, Tag


def get_product_type_stat(type_id: str, **_) -> Dict[str, Any]:
    result = products_repository.get_type_stat(type_id)
    if not result:
        abort(404, "Product type not found")
    return result


def get_products_by_type(
        product_type: str, tags: Set[str] = None,
        min_price: int = None, max_price: int = None,
        min_stars: int = None, max_stars: int = None,
        characteristics: Dict[str, Dict[str, Any]] = None, **_
) -> List[Dict[str, Any]]:
    if not products_repository.get_type_by_id(product_type):
        abort(404, "Product type not found")
    products = products_repository.get_products_by_type(
        product_type, tags, min_price, max_price, min_stars, max_stars, characteristics
    )
    return [
        {
            **product[0].as_dict,
            "picture": product[1].link if product[1] else None,
            "stars_avg": product[2],
            "type": product[0].type_ref
        }
        for product in products
    ]


def get_product_info(user_id: str, product_id: str, **_) -> Dict[str, Any]:
    result = products_repository.get_full_product_by_id(product_id)
    if not result:
        abort(404, "Product not found")
    product, feedback = result
    return {
        **product.as_dict,
        "stars_avg": (sum(feedback_item.stars for feedback_item in feedback) / len(feedback)) if feedback else None,
        "type": product.type_ref, "pictures": product.pictures,
        "feedback": [
            {**i.as_dict, "user_name": f"{i.user_ref.first_name} {i.user_ref.last_name}", "deletable": i.user_ref.id == user_id}
            for i in feedback
        ]
    }


def get_tags(**_) -> List[Tag]:
    return products_repository.get_all_tags()


def get_product_types(**_) -> List[Dict[str, str]]:
    return [product_type.as_dict for product_type in products_repository.get_types()]
