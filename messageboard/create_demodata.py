# create_demodata.py

from datetime import datetime

# From message board
from .db_models import Categories, Users

# Create few categories
general = Categories(
    category_name = "General",
    category_description = "General discussion about almost everything.",
    category_secret = False,
    category_created = datetime.now()
)

coding = Categories(
    category_name = "Coding",
    category_description = "Ask about coding here.",
    category_secret = False,
    category_created = datetime.now()
)

secret = Categories(
    category_name = "Secret",
    category_description = "This category is not visible for everyone!",
    category_secret = True,
    category_created = datetime.now()
)

# Create one admin and few users
# PW: admin
admin = Users(
    username = "Admin",
    password_hash = "sha256$b28kBRwL$604a9e44ab541f9ef993dd170eef56e4713cf72681b0ced81416175a02a19634",
    email = "admin@messageboard.com",
    user_role = "ADMIN",
    account_created = datetime.now(),
    last_login = datetime.now()
)

# PW: johndoe
john_doe = Users(
    username = "John Doe",
    password_hash = "sha256$cwoNNh4F$f06ffe21c21b8a1dc3b5456efc5d086bfa8e8584d37473344a468105d519c19e",
    email = "john.doe@messageboard.com",
    user_role = "USER",
    account_created = datetime.now(),
    last_login = datetime.now()
)

# PW: janedoe
jane_doe = Users(
    username = "Jane Doe",
    password_hash = "sha256$ivlIjuur$207a6e2441576f269b8be79fcee47876d729c36cff483dc35e865e2ef25e1f63",
    email = "jane.doe@messageboard.com",
    user_role = "SECRET",
    account_created = datetime.now(),
    last_login = datetime.now()
)
