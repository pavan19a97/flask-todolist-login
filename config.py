import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/Logging'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
