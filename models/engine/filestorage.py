#!/usr/bin/python3
import json


class FileStorage:
    __file = "file.json"
    __objects = {}

    def all(self, cls=None):
        """return all the current objects in the __objects"""
        if cls is not None:
            return {key: value for key, value in self.__objects.items()
                    if key.split(".")[0] == cls}
        return self.__objects

    def new(self, obj):
        """add a new object to the __object variable"""
        dict_ = {f"{obj.__class__.__name__}" + '.' + f"{obj.id}": obj}
        self.__objects.update(dict_)

    def save(self):
        """serialize the object to a json file and saved at __file"""
        from datetime import datetime
        with open(self.__file, 'w', encoding="utf-8") as file:
            newDict = {}
            newDict.update(self.__objects)
            for key, value in newDict.items():
                newDict[key] = value.to_dict()
            json.dump(newDict, file, indent=4)

    def reload(self):
        """deserialize json file to an object"""
        from models.rooms import Room
        from models.users import User
        from models.messages import Message
        from models.reviews import Review
        objs = {}
        try:
            with open(self.__file, 'r', encoding='utf-8') as file:
                objs = json.load(file)
                for key, value in objs.items():
                    self.__objects[key] = eval(value['__class__'])(**value)
        except FileNotFoundError:
            pass

    def delete(self, obj):
        """delete an object from the __objects"""
        obj_key = obj.__class__.__name__ + '.' + obj.id
        if obj_key in self.__objects:
            del self.__objects[obj_key]
            self.save()

    def close(self):
        """deserializes json file to object"""
        self.reload()

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
