import os

SQLALCHEMY_DATABASE_URI = "mysql://flask:pass@mysql/flask"
SECRET_KEY = os.urandom(24)
SNAPS_DIRECTORY = "./snaps"
SNAP_TIME_LAG = 40
SQLALCHEMY_TRACK_MODIFICATIONS = False