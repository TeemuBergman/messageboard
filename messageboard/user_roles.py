# user_roles.py

from enum import Enum, auto
from functools import wraps
from flask import current_app
from flask_login import current_user


class Role(Enum):
    DELETED = auto()
    BANNED = auto()
    USER = auto()
    SECRET = auto()
    ADMIN = auto()


# Login_required with roles
def login_required(role = Role.USER):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            # Check if user has logged in
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            # Hierarchy tree (highest value means admin rights)
            if role.value <= Role[current_user.user_role].value and role.value <= Role.ADMIN.value:
                pass
            elif role.value <= Role[current_user.user_role].value and role.value <= Role.SECRET.value:
                pass
            elif role.value == Role[current_user.user_role].value and role.value == Role.USER.value:
                pass
            elif role.value == Role[current_user.user_role].value and role.value == Role.BANNED.value:
                pass
            elif role.value == Role[current_user.user_role].value and role.value == Role.DELETED.value:
                pass
            else:
                return current_app.login_manager.unauthorized()

            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


# Check if current user can view secret categories
def check_secret():
    if current_user.is_authenticated:
        return Role[current_user.user_role].value >= Role.SECRET.value
    return False


# Check if current user can post
def check_post():
    if current_user.is_authenticated:
        return Role[current_user.user_role].value <= Role.BANNED.value
    return False
