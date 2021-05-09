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


class Product(Base, ImprovedBase):
    __tablename__ = 'goods'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(128), nullable=False, unique=True)
    description = Column(String(2048), nullable=False, unique=True)
    characteristics = Column(JSON(), nullable=False)
    type = Column(UUID(), ForeignKey('goods_types.id', ondelete='NO ACTION'), nullable=False)
    price = Column(Integer(), nullable=False)


class ProductType(Base, ImprovedBase):
    __tablename__ = 'goods_types'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(128), nullable=False, unique=True)
    picture = Column(String(1024), nullable=False)


class Tag(Base, ImprovedBase):
    __tablename__ = 'tags'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(128), nullable=False, unique=True)


class ProductPicture(Base, ImprovedBase):
    __tablename__ = 'product_pictures'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    link = Column(String(1024), nullable=False)


class CartItem(Base, ImprovedBase):
    __tablename__ = 'cart_items'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False, unique=True)
    user_id = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)


class WishListItem(Base, ImprovedBase):
    __tablename__ = 'wishlist'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False, unique=True)
    user_id = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)


class Feedback(Base, ImprovedBase):
    __tablename__ = 'feedback'

    id = Column(UUID(), nullable=False, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(UUID(), ForeignKey('goods.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    body = Column(String(4096), nullable=False)
    stars = Column(SmallInteger(), nullable=False)
