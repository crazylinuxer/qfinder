from typing import List, Union

from repository import db, CartItem, WishListItem, Feedback, Product


def add_item(item: Union[CartItem, WishListItem, Feedback]) -> None:
    db.session.merge(item)
    db.session.commit()


def delete_item(item: Union[CartItem, WishListItem, Feedback]) -> None:
    db.session.delete(item)
    db.session.commit()


def get_cart_content(user_id: str) -> List[Product]:
    return db.session.query(Product).filter(Product.id == CartItem.product_id).\
        filter(CartItem.user_id == user_id).all()


def get_wishlist_content(user_id: str) -> List[Product]:
    return db.session.query(Product).filter(Product.id == WishListItem.product_id).\
        filter(WishListItem.user_id == user_id).all()


def get_cart_item(user_id: str, product_id: str) -> CartItem:
    return db.session.query(CartItem).filter(CartItem.user_id == user_id).\
        filter(CartItem.product_id == product_id).first()


def get_wishlist_item(user_id: str, product_id: str) -> WishListItem:
    return db.session.query(WishListItem).\
        filter(WishListItem.user_id == user_id).\
        filter(WishListItem.product_id == product_id).first()


def get_feedback(feedback_id: str) -> Feedback:
    return db.session.query(Feedback).filter(Feedback.id == feedback_id).first()
