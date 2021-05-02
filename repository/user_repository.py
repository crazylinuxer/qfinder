from typing import List

from sqlalchemy import or_

from . import db, User


def add_or_edit_user(user: User) -> User:
    db.session.merge(user)
    db.session.commit()
    return user


def delete_user(user: User) -> None:
    db.session.delete(user)
    db.session.commit()


def search_user(name_part: str) -> List[User]:
    name_part = "%{}%".format(name_part)
    return db.session.query(User).filter(or_(User.first_name.ilike(name_part), User.last_name.ilike(name_part))).all()


def get_user_by_email(email: str) -> User:
    return db.session.query(User).filter(User.email == email).first()


def get_user_by_id(user_id: str) -> User:
    return db.session.query(User).filter(User.id == user_id).first()
