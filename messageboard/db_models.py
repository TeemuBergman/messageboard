# db_models.py

import click
from flask.cli import with_appcontext
from flask_login import UserMixin
from . import db


# Defining user model
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), nullable = False)
    password_hash = db.Column(db.String(256), nullable = False)
    email = db.Column(db.String(256), nullable = False, unique = True)
    account_created = db.Column(db.DateTime, nullable = False)
    last_login = db.Column(db.DateTime, nullable = False)
    banned = db.Column(db.Boolean, default = False)
    ban_duration = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default = False)
    view_secret = db.Column(db.Boolean, default = False)
    deleted = db.Column(db.Boolean, default = False)

    def get_id(self):
        return self.user_id


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
    thread_visible = db.Column(db.Boolean, nullable = False)
    thread_name = db.Column(db.String(256), unique = True, nullable = False)
    thread_created = db.Column(db.DateTime, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))


# Defining message model
class Messages(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key = True)
    message_content = db.Column(db.String, nullable = False)
    message_created = db.Column(db.DateTime, nullable = False)
    thread_id = db.Column(db.Integer, db.ForeignKey("threads.thread_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))


# CLI command for DB initialize
@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
