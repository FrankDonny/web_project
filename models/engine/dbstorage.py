#!/usr/bin/python3
"""date base module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# from os import getenv
# import json

username = "MYSELF"
password = "MY_PASS"
host = "HOST"
dataB = "MY_DATABASE"


class DBStorage:
    __engine = None
    __session = None
    # __objects = {}

    def __init__(self):
        """initializing the class by creating the session engine"""
        self.__engine = create_engine('mysql+mysqldb://web_app_user:pass@localhost:3306/web_app_DB',
                                      pool_pre_ping=True)

    def all(self, cls=None):
        """retrieves all objects relating to either a class or not"""
        from models.rooms import Room
        from models.users import User
        from models.messages import Message
        from models.reviews import Review

        classes = {"User": User, "Room": Room, "Message": Message,
                   "Review": Review}
        new_dict = {}
        for clss in classes:
            if cls is None:  # or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
            else:
                objs = self.__session.query(classes[cls]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """adds a new instance of a class to the current session"""
        # dict_ = {f"{obj.__class__.__name__}" + '.' + f"{obj.id}": obj}
        # self.__objects.update(dict_)
        self.__session.add(obj)

    def save(self):
        """saves the current session"""
        self.__session.commit()
        #backup the database with a file storage
        # with open("new_json.json", 'w', encoding="utf-8") as file:
        #     newDict = {}
        #     newDict.update(self.__objects)
        #     for key, value in newDict.items():
        #         newDict[key] = value.to_dict()
        #     json.dump(newDict, file, indent=4)

    def reload(self):
        """to create all tables"""
        from models.basemodel import Base
        from models.rooms import Room
        from models.users import User
        from models.messages import Message
        from models.reviews import Review

        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def delete(self, obj=None):
        """delete an object from the current session"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def close(self):
        """closes/clears a session"""
        self.__session.close()

    def get(self, cls, id):
        """retrieves an object base on its id"""
        objs = self.all(cls)
        for key, value in objs.items():
            if key.split('.')[1] == id:
                return value

    def count(self, cls):
        """count the number objects of a class"""
        count = 0
        objs = self.all(cls)
        for _ in objs:
            count += 1
        return count
