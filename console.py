#!/usr/bin/python3
"""command line module"""
from cmd import Cmd
from datetime import datetime

from models import storage
from models.messages import Message
from models.reviews import Review
from models.rooms import Room
from models.users import User

classes = ["User", "Room", "Review", "Message"]


class WebApp(Cmd):
    """command line tool"""
    prompt = 'Donny_$ '

    def emptyline(self):
        """moves to the next line"""
        pass

    def do_EOF(self, _):
        """implementation of End of File"""
        return True

    def do_quit(self, _):
        exit()

    def do_create(self, line):
        """create a new object"""
        if len(line) == 0:
            print('** provide a class name **')
            return
        line_split = line.split()
        if line_split[0] not in classes:
            print('** incorrect class **')
            return
        obj = eval(line_split[0] + '()')
        for ob in line_split[1:]:
            if '=' not in ob:
                continue
            ob_split = ob.split('=')
            value = ob_split[1].strip('"').replace('_', ' ')
            try:
                value = int(value)
            except Exception:
                pass
            setattr(obj, ob_split[0], value)
        storage.new(obj)
        storage.save()
        print(obj.id)

    def help_create(self):
        """help function for <create>"""
        print("USAGE: "
              "create <class_name> => creates a new instance")

    def do_update(self, line):
        """update an object"""
        if len(line) == 0:
            print('** provide a class name **')
            return
        line_split = line.split()
        if line_split[0] not in classes:
            print('** incorrect class **')
            return
        if len(line_split) == 1:
            print("** provide an instance id **")
            return
        value = [val.split('.')[1] for val in storage.all(line_split[0])]
        obj = storage.get(line_split[0], line_split[1])
        for ob in line_split[2:]:
            if '=' not in ob:
                continue
            ob_split = ob.split('=')
            setattr(obj, ob_split[0], ob_split[1].strip('"').replace('_', ' '))
        setattr(obj, "updated_at", datetime.now())
        storage.save()
        print(obj.id)

    def help_update(self):
        """update help function"""
        print("USAGE: "
              'update <class_name> <object_id> new_key="new_value"'
              'new_key="new_value" ...')

    def do_delete(self, line):
        """delete an object"""
        if len(line) == 0:
            print('** provide a class name **')
            return
        line_split = line.split()
        if len(line_split) == 1:
            print("** provide the class id **")
            return
        objs = storage.all(line_split[0])
        # print(line_split[0]+'.'+line_split[1])
        if (line_split[0]+'.'+line_split[1]) in objs.keys():
            storage.delete(objs[line_split[0]+'.'+line_split[1]])

    def help_delete(self):
        """help function for <delete>"""
        print("USAGE: "
              "delete <class_name> <object_id> => deletes an object based on"
              "the class and the it's id")

    def do_show(self, line):
        """show the string representation of an object"""
        if len(line) == 0:
            print('** provide a class name **')
            return
        line_split = line.split()
        if len(line_split) == 1:
            print("** provide the class id **")
            return
        objs = storage.all(line_split[0])
        if (line_split[0] + '.' + line_split[1]) in objs.keys():
            print(objs[line_split[0] + '.' + line_split[1]])

    def help_show(self):
        """help function for <show>"""
        print("USAGE: "
              "show <class_name> <object_id> => outputs an object based on the"
              "class and the it's id")

    def do_all(self, line):
        """return all objects in storage"""
        if len(line) == 0:
            objs = storage.all()
            for key, value in objs.items():
                print(value)
        else:
            line_split = line.split()
            objs = storage.all(line_split[0])
            for value in objs.values():
                print(value)

    def help_all(self):
        """help function for <all>"""
        print("USAGE: "
              "all => outputs all instances available\n"
              "all <class_name> => outputs all instances based on the class")


if __name__ == "__main__":
    WebApp().cmdloop()
