# commands.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Defining user model
class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, nullable = False)
    email = db.Column(db.String(256), unique = True, nullable = False)
    password_hash = db.Column(db.String(256), nullable = False)
    account_created = db.Column(db.DateTime, nullable = False)
    last_login = db.Column(db.DateTime, nullable = False)
    banned = db.Column(db.Boolean, nullable = False)
    ban_duration = db.Column(db.DateTime, nullable = False)
    is_admin = db.Column(db.Boolean, nullable = False)
    secret = db.Column(db.Boolean, nullable = False)

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
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))


# Defining message model
class Messages(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key = True)
    message_content = db.Column(db.String, nullable = False)
    message_created = db.Column(db.DateTime, nullable = False)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.thread_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))


with app.app_context():
    db.create_all()