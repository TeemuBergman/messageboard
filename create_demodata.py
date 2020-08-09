# commands.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .messageboard.db_models import Categories
from .messageboard.tools import getTime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Create demo data for database

general = Categories(
    category_name = "General",
    category_description = "General discussion about almost everything",
    category_secret = False,
    category_created = getTime()
)

coding = Categories(
    category_name = "Coding",
    category_description = "Ask about coding here!",
    category_secret = False,
    category_created = getTime()
)

db.session.add(general, coding)
db.session.commit()
