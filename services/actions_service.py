from typing import List, Dict, Union, Any

from repository import actions_repository, CartItem, WishListItem, Feedback


def add_to_cart(user_id: str, product_id: str, **_) -> None:
    pass


def get_cart_content(user_id: str, **_) -> Dict[str, Union[int, List[dict]]]:
    pass


def remove_from_cart(user_id: str, product_id: str, **_) -> None:
    pass


def add_to_wishlist(user_id: str, product_id: str, **_) -> None:
    pass


def get_wishlist_content(user_id: str, **_) -> Dict[str: Union[str, int]]:
    pass


def remove_from_wishlist(user_id: str, product_id: str, **_) -> None:
    pass


def leave_feedback(user_id: str, product_id: str, stars: int, body: str, **_) -> None:
    pass


def remove_feedback(user_id: str, feedback_id: str, **_) -> None:
    pass
