#!/usr/bin/python3
from models import storage
from models.basemodel import BaseModel
from models.users import Users


all_objs = storage.all('Users')
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

# print("-- Create a new object --")
# my_model = BaseModel()
# my_model.name = "My_First_Model"
# my_model.my_number = 89
# my_model.save()
# print(my_model)

# print("-- Create a new object --")
# my_model = Users()
# my_model.first_name = "Frank"
# my_model.last_name = "Arkoh"
# my_model.save()
# print(my_model)
