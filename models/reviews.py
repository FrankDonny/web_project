#!/usr/bin/python3
"""messages table module"""
from models.basemodel import BaseModel, Base
from sqlalchemy import String, ForeignKey, Column


class Review(BaseModel, Base):
    """Messages class"""
    __tablename__ = 'review'
    text = Column(String(120))
    user_id = Column(String(60), ForeignKey("user.id"), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes review"""
        super().__init__(*args, **kwargs)
