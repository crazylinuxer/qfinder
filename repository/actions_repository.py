from typing import List

from repository import CartItem, WishListItem, Feedback


def add_cart_item(item: CartItem) -> None:
    pass


def get_cart_content(user_id: str) -> List[CartItem]:
    pass


def get_cart_item(user_id: str, product_id: str) -> CartItem:
    pass


def delete_cart_item(item: CartItem) -> None:
    pass


def add_wishlist_item(item: WishListItem) -> None:
    pass


def get_wishlist_content(user_id: str) -> List[WishListItem]:
    pass


def get_wishlist_item(user_id: str, product_id: str) -> WishListItem:
    pass


def delete_wishlist_item(item: WishListItem) -> None:
    pass


def add_feedback_item(item: Feedback) -> None:
    pass


def get_feedback(feedback_id: str) -> Feedback:
    pass


def delete_feedback(feedback: Feedback) -> None:
    pass
