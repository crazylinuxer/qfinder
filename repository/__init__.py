import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.state import InstanceState
from sqlalchemy import (inspect, Column, String, SmallInteger,
                        Boolean, CheckConstraint, ForeignKey,
                        DateTime, Index, JSON, Integer)

from app_creator import app


db = SQLAlchemy(app)
Base = declarative_base()


class ImprovedBase:
    @property
    def as_dict(self):
        return {
            c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs
            if not isinstance(getattr(self, c.key), InstanceState)
        }


class User(Base, ImprovedBase):
    __tablename__ = 'users'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(512), nullable=False)
    last_name = Column(String(512), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(64), nullable=False)

    feedback = relationship("Feedback", back_populates='user_ref', primaryjoin="Feedback.user_id == User.id")
    cart = relationship("CartItem", back_populates='user_ref', primaryjoin="CartItem.user_id == User.id")
    wishlist = relationship("WishListItem", back_populates='user_ref', primaryjoin="WishListItem.user_id == User.id")


class Product(Base, ImprovedBase):
    __tablename__ = 'products'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(2048), nullable=False, unique=True)
    characteristics = Column(JSON(), nullable=False)
    type = Column(UUID(), ForeignKey('goods_types.id', ondelete='NO ACTION'), nullable=False)
    price = Column(Integer(), nullable=False)

    type_ref = relationship("ProductType", back_populates='products', foreign_keys=type)

    tags = relationship("TagToProduct", back_populates='product_ref', primaryjoin="TagToProduct.product_id == Product.id")
    feedback = relationship("Feedback", back_populates='product_ref', primaryjoin="Feedback.product_id == Product.id")
    cart_occurrences = relationship("CartItem", back_populates='product_ref', primaryjoin="CartItem.product_id == Product.id")
    wishlist_occurrences = relationship("WishListItem", back_populates='product_ref',
                                        primaryjoin="WishListItem.product_id == Product.id")
    pictures = relationship("ProductPicture", back_populates='product_ref',
                            primaryjoin="ProductPicture.product_id == Product.id")


class ProductType(Base, ImprovedBase):
    __tablename__ = 'product_types'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(128), nullable=False, unique=True)
    picture = Column(String(1024), nullable=False)

    products = relationship("Product", back_populates='type_ref', primaryjoin="ProductType.id == Product.type")


class Tag(Base, ImprovedBase):
    __tablename__ = 'tags'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(128), nullable=False, unique=True)

    products = relationship("TagToProduct", back_populates='tag_ref', primaryjoin="TagToProduct.product_id == Tag.id")


class TagToProduct(Base, ImprovedBase):
    __tablename__ = 'tags_to_products'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    tag_id = Column(UUID(), ForeignKey('tags.id', ondelete='CASCADE'), nullable=False)

    product_ref = relationship("Product", back_populates='tags', foreign_keys=product_id)
    tag_ref = relationship("Tag", back_populates='products', foreign_keys=tag_id)


class ProductPicture(Base, ImprovedBase):
    __tablename__ = 'product_pictures'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    link = Column(String(1024), nullable=False)

    product_ref = relationship("Product", back_populates='pictures', foreign_keys=product_id)


class CartItem(Base, ImprovedBase):
    __tablename__ = 'cart_items'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False, unique=True)
    user_id = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    product_ref = relationship("Product", back_populates='cart_occurrences', foreign_keys=product_id)
    user_ref = relationship("User", back_populates='cart', foreign_keys=user_id)


class WishListItem(Base, ImprovedBase):
    __tablename__ = 'wishlist'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False, unique=True)
    user_id = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    product_ref = relationship("Product", back_populates='wishlist_occurrences', foreign_keys=product_id)
    user_ref = relationship("User", back_populates='wishlist', foreign_keys=user_id)


class Feedback(Base, ImprovedBase):
    __tablename__ = 'feedback'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    body = Column(String(4096), nullable=False)
    stars = Column(SmallInteger(), nullable=False)

    feedback_stars_check = CheckConstraint('(stars <= 5 AND stars >= 0)', name='feedback_stars_check')

    product_ref = relationship("Product", back_populates='feedback', foreign_keys=product_id)
    user_ref = relationship("User", back_populates='feedback', foreign_keys=user_id)
