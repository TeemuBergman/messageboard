# create_database.py

from flask import Flask
from messageboard.db_models import Categories, Threads, Messages, Users
from messageboard import db

app = Flask(__name__)
db.init_app(app)

with app.app_context():
    db.session.add(Categories)
    db.session.add(Threads)
    db.session.add(Messages)
    db.session.add(Users)
    db.session.commit()
