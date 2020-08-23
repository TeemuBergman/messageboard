# config.py

from os import getenv


class Config:
    # Config variables
    TESTING = False
    DEBUG = False
    FLASK_ENV = "development"
    SECRET_KEY = getenv("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Database config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
