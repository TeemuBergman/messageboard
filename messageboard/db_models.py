# db_models.py

from flask_login import UserMixin

# From message board
from . import db


# Defining user model
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), nullable = False)
    user_role = db.Column(db.String(64), nullable = False)
    password_hash = db.Column(db.String(256), nullable = False)
    email = db.Column(db.String(256), nullable = False, unique = True)
    account_created = db.Column(db.DateTime, nullable = False)
    last_login = db.Column(db.DateTime, nullable = False)
    banned = db.Column(db.Boolean, default = False)
    ban_duration = db.Column(db.DateTime)
    admin = db.Column(db.Boolean, default = False)
    view_secret = db.Column(db.Boolean, default = False)
    deleted = db.Column(db.Boolean, default = False)

    def get_id(self):
        return self.user_id

    def get_user_role(self):
        return self.user_role


# Defining category model
class Categories(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key = True)
    category_secret = db.Column(db.Boolean, nullable = False)
    category_name = db.Column(db.String(256), unique = True, nullable = False)
    category_description = db.Column(db.String(256), nullable = False)
    category_created = db.Column(db.DateTime, nullable = False)


# Defining thread model
class Threads(db.Model):
    __tablename__ = "threads"
    thread_id = db.Column(db.Integer, primary_key = True)
    thread_name = db.Column(db.String(256), nullable = False)
    thread_created = db.Column(db.DateTime, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))


# Defining message model
class Messages(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key = True)
    message_content = db.Column(db.String, nullable = False)
    message_created = db.Column(db.DateTime, nullable = False)
    message_edited = db.Column(db.DateTime)
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.thread_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
