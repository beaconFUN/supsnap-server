import os
import binascii
import datetime
from db import db
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Beacon(Base):
    __tablename__ = "beacon"
    id = Column(Integer, primary_key=True)
    uuid = Column(Unicode(36))
    major = Column(Integer)
    minor = Column(Integer)
    
    place = relation("Place")
    
    def __init__(self, uuid, major, minor):
        self.uuid = uuid
        self.major = major
        self.minor = minor

class Place(Base):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    beacon = Column(Integer, ForeignKey("beacon.id"))
    
    def __init__(self, name, beacon):
        self.name = name
        self.beacon = beacon

class Visiter(Base):
    __tablename__ = "visiter"
    id = Column(Integer, primary_key=True)
    user = Column(Unicode(255))
    place = Column(Integer, ForeignKey("place.id"))
    pass_phrase = Column(Unicode(32))
    snap = Column(Integer, ForeignKey("snap.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, user, place, snap):
        self.user = user
        self.place = place
        self.pass_phrase = genPassPhrase()
    
    def genPassPhrase():
        return binascii.hexlify(os.urandom(16))

class Snap(Base):
    __tablename__ = "snap"
    id = Column(Integer, primary_key=True)
    src = Column(Unicode(255))
    thum_src = Column(Unicode(255))
    date = Column(DateTime)

    visiters = relation("Visiter", backref="snap")
    
    def __init__(self, datetime):
        self.src = None
        self.thum_src = None
        self.date = datetime


def init():
    db.create_all()