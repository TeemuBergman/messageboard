# config.py

from os import getenv, path
# from dotenv import load_dotenv


class Config:
    # Config variables
    TESTING = False
    DEBUG = False
    FLASK_ENV = 'development'
    SECRET_KEY = getenv('SECRET_KEY')
    # SESSION_COOKIE_NAME = getenv('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    # DATABASE_URI = os.environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    # DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
