from typing import List, Dict, Any

from repository import products_repository, Tag


def get_products_by_type(
        product_type: str, tags: List[str] = None,
        min_price: int = None, max_price: int = None,
        min_stars: int = None, max_stars: int = None
) -> List[Dict[str, Any]]:
    pass


def get_product_info(product_id: str) -> Dict:
    pass


def get_tags() -> List[Tag]:
    pass
