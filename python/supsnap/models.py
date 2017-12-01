import os
import binascii
import datetime
from db import db
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relationship

class Beacon(db.Model):
    __tablename__ = "beacon"
    id = Column(Integer, primary_key=True)
    uuid = Column(Unicode(36))
    major = Column(Integer)
    minor = Column(Integer)
    
    place = relationship("Place", uselist=False)
    
    def __init__(self, uuid, major, minor):
        self.uuid = uuid
        self.major = major
        self.minor = minor

class Place(db.Model):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255))
    beacon = Column(Integer, ForeignKey("beacon.id"))
    
    camera = relationship("Camera")
    
    def __init__(self, name, beacon):
        self.name = name
        self.beacon = beacon

class Visiter(db.Model):
    __tablename__ = "visiter"
    id = Column(Integer, primary_key=True)
    user = Column(Unicode(255))
    place = Column(Integer, ForeignKey("place.id"))
    pass_phrase = Column(Unicode(32))
    snap = Column(Integer, ForeignKey("snap.id"))
    date = Column(DateTime)
    
    def __init__(self, user, place, snap):
        self.user = user
        self.place = place
        self.pass_phrase = self.genPassPhrase()
        self.snap = snap
        self.date = datetime.datetime.now().replace(microsecond=0)
    
    def genPassPhrase(self):
        return binascii.hexlify(os.urandom(16))

class Snap(db.Model):
    __tablename__ = "snap"
    id = Column(Integer, primary_key=True)
    src = Column(Unicode(255))
    thum_src = Column(Unicode(255))
    date = Column(DateTime)
    
    visiters = relationship("Visiter")
    
    def __init__(self, datetime):
        self.src = None
        self.thum_src = None
        self.date = datetime

class Camera(db.Model):
    __tablename__ = "camera"
    id = Column(Integer, primary_key=True)
    place = Column(Integer, ForeignKey("place.id"))
    endpoint = Column(Unicode(255))
    
    def __init__(self, place, endpoint):
        self.place = place
        self.endpoint = endpoint


def init():
    db.create_all()