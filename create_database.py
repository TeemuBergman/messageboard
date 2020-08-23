# create_database.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from messageboard.db_models import Categories, Threads, Messages, Users

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

Categories.db.create_all()
Threads.db.create_all()
Messages.db.create_all()
Users.db.create_all()
