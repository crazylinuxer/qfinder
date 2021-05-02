from typing import Tuple

from flask_jwt_extended import create_access_token, create_refresh_token
from flask import abort
from bcrypt import gensalt, hashpw, checkpw

from repository import user_repository, User


def check_password(password: str):
    letters = bytes(range(b'a'[0], b'z'[0]+1)).decode()
    lower = False
    upper = False
    digit = False
    for letter in password:
        check = False
        if letters.find(letter) != -1:
            check = True
            lower = True
        if letters.upper().find(letter) != -1:
            check = True
            upper = True
        if "-.?!@=_^:;#$%&*()+\\<>~`/\"'".find(letter) != -1:
            check = True
        if letter.isdigit():
            check = True
            digit = True
        if not check:
            abort(422, f"Password cannot contain symbols like this: '{letter}'")
    if not lower:
        abort(422, "Password must contain at least one lowercase letter")
    if not upper:
        abort(422, "Password must contain at least one uppercase letter")
    if not digit:
        abort(422, "Password must contain at least one digit")


def auth_user(email: str, password: str) -> Tuple[str, str]:
    user = user_repository.get_user_by_email(email)
    if not user:
        abort(404, "User not found")
    if not checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        abort(401, "Invalid credentials given")
    return create_access_token(identity=user.id), create_refresh_token(identity=user.id)


def register_user(email: str, first_name: str, last_name: str, password: str, **_):
    check_password(password)
    if user_repository.get_user_by_email(email) is not None:
        abort(409, "User with this email already exists")
    user = User()
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.password_hash = hashpw(password.encode('utf-8'), gensalt(12)).decode()
    user_repository.add_or_edit_user(user)


def get_user_account(user_id: str) -> User:
    return user_repository.get_user_by_id(user_id)


def edit_user_account(user_id: str, email: str = None, first_name: str = None, last_name: str = None, **_) -> User:
    user = user_repository.get_user_by_id(user_id)
    user.email = email or user.email
    user.first_name = first_name or user.first_name
    user.last_name = last_name or user.last_name
    user_repository.add_or_edit_user(user)
    return user
