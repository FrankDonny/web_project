#!/usr/bin/python3
"""messages table module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import String, ForeignKey, Column
from sqlalchemy.orm import relationship


class Room(BaseModel, Base):
    """room class"""
    __tablename__ = "room"
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(1024), nullable=False)
    creator_id = Column(String(60), ForeignKey("user.id"), nullable=False)
    # member_name = Column(String(60), ForeignKey("user.name),
    # nullable=False"), nullable=False)
    messages = relationship("Message", backref="room",
                            cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes room"""
        super().__init__(*args, **kwargs)
