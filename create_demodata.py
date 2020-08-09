# create_demodata.py

import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Defining category model
class Categories(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key = True)
    category_secret = db.Column(db.Boolean, nullable = False)
    category_name = db.Column(db.String(256), unique = True, nullable = False)
    category_description = db.Column(db.String(256), nullable = False)
    category_created = db.Column(db.DateTime, nullable = False)

# Create demo data for database

general = Categories(
    category_name = "General",
    category_description = "General discussion about almost everything",
    category_secret = False,
    category_created = datetime.now()
)

coding = Categories(
    category_name = "Coding",
    category_description = "Ask about coding here!",
    category_secret = False,
    category_created = datetime.now()
)

db.session.add(general, coding)
db.session.commit()
