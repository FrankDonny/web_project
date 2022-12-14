#!/usr/bin/python3
"""basemodel module for all tables"""
from uuid import uuid4
from datetime import datetime
from models import storage
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime

Base = declarative_base()


class BaseModel:
    """The basemodel class to be inherited from other models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializing instances of the object"""
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                setattr(self, key, value)
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """saves the object"""
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """converts the object to a dictionary"""
        newDict = self.__dict__.copy()
        newDict['created_at'] = self.created_at.isoformat()
        newDict['updated_at'] = self.created_at.isoformat()
        newDict.update({"__class__": self.__class__.__name__})
        if '_sa_instance_state' in newDict.keys():
            del newDict["_sa_instance_state"]
        if "password" in newDict.keys():
            del newDict["password"]
        return newDict

    def delete(self):
        """delete the current instance"""
        storage.delete(self)

    def __str__(self):
        """the string representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"
