# create_database.py

from messageboard.db_models import Categories, Threads, Messages, Users
from messageboard import db

db.session.add(Categories)
db.session.add(Threads)
db.session.add(Messages)
db.session.add(Users)
db.session.commit()
