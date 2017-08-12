import os

SQLALCHEMY_DATABASE_URI = "mysql://flask:pass@mysql/flask"
SECRET_KEY = os.urandom(24)