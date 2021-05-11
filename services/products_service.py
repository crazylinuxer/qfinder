from typing import List, Dict, Set, Any

from repository import products_repository, Tag


def get_product_type_stat(type_id: str, **_) -> Dict[str, Any]:
    pass


def get_products_by_type(
        product_type: str, tags: Set[str] = None,
        min_price: int = None, max_price: int = None,
        min_stars: int = None, max_stars: int = None, **_
) -> List[Dict[str, Any]]:
    pass


def get_product_info(product_id: str, **_) -> Dict:
    pass


def get_tags(**_) -> List[Tag]:
    pass


def get_product_types(**_) -> List[Dict[str, str]]:
    pass
