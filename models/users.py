#!/usr/bin/python3
"""User table module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from os import getenv


class User(BaseModel, Base):
    """User class"""
    __tablename__ = "user"
    name = Column(String(60), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(60), nullable=False)
    number = Column(String(15))
    rooms_created = relationship("Room", backref="user",
                                 cascade="all, delete, delete-orphan")
    # joined_rooms = relationship("Room", backref="member",
    # cascade="all, delete, delete-orphan")
    messages = relationship("Message", backref="user",
                            cascade="all, delete, delete-orphan")
    reviews = relationship("Review", backref="user",
                           cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
