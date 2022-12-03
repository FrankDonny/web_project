#!/usr/bin/python3
"""messages table module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import String, ForeignKey, Column
from os import getenv


class Message(BaseModel, Base):
    """Messages class"""
    __tablename__ = 'message'
    text = Column(String(4096))
    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    room_id = Column(String(60), ForeignKey("room.id"), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes message"""
        super().__init__(*args, **kwargs)
