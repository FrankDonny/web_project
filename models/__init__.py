#!/usr/bin/python3
from os import getenv

if getenv("DATABASE_TYPE") == "db":
    from models.engine.dbstorage import DBStorage
    storage = DBStorage()
else:
    from models.engine.filestorage import FileStorage
    storage = FileStorage()
storage.reload()
