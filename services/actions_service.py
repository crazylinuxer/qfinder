from typing import List, Dict, Union

from flask import abort

from repository import actions_repository, CartItem, WishListItem, Feedback


def add_to_cart(user_id: str, product_id: str, **_) -> None:
    item = CartItem()
    item.user_id = user_id
    item.product_id = product_id
    actions_repository.add_item(item)


def get_cart_content(user_id: str, **_) -> Dict[str, Union[int, List[dict]]]:
    cart = actions_repository.get_cart_content(user_id)
    content = [{**product.as_dict, "picture": product.pictures.link} for product in cart]  # todo check for sanity
    price = sum(product.price for product in cart)
    return {"content": content, "total_price": price}


def remove_from_cart(user_id: str, product_id: str, **_) -> None:
    cart_item = actions_repository.get_cart_item(user_id, product_id)
    if not cart_item:
        abort(404, "Cart entry not found")
    actions_repository.delete_item(cart_item)


def add_to_wishlist(user_id: str, product_id: str, **_) -> None:
    item = WishListItem()
    item.user_id = user_id
    item.product_id = product_id
    actions_repository.add_item(item)


def get_wishlist_content(user_id: str, **_) -> List[Dict[str, Union[str, int]]]:
    wishlist = actions_repository.get_wishlist_content(user_id)
    return [{**product.as_dict, "picture": product.pictures.link} for product in wishlist]  # todo check for sanity


def remove_from_wishlist(user_id: str, product_id: str, **_) -> None:
    wishlist_item = actions_repository.get_wishlist_item(user_id, product_id)
    if not wishlist_item:
        abort(404, "WishList entry not found")
    actions_repository.delete_item(wishlist_item)


def leave_feedback(user_id: str, product_id: str, stars: int, body: str, **_) -> None:
    item = Feedback()
    item.stars = stars
    item.body = body
    item.user_id = user_id
    item.product_id = product_id
    actions_repository.add_item(item)


def remove_feedback(user_id: str, feedback_id: str, **_) -> None:
    feedback_item = actions_repository.get_feedback(feedback_id)
    if not feedback_item or feedback_item.user_id != user_id:
        abort(404, "Feedback not found")
    actions_repository.delete_item(feedback_item)
