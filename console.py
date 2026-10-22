#!/usr/bin/python3
"""Defines the HBNBCommand console interpreter."""
import cmd
import shlex
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB."""
    prompt = '(hbnb) '
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print()
        return True

    def emptyline(self):
        """Overriding emptyline to do nothing."""
        pass

    def do_create(self, arg):
        """Creates a new instance of a class with given parameters and saves it."""
        try:
            args = shlex.split(arg)
        except Exception:
            args = arg.split()

        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        new_instance = HBNBCommand.__classes[class_name]()

        for param in args[1:]:
            if "=" not in param:
                continue
            key, value = param.split("=", 1)

            # Parse string values
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('_', ' ').replace('\\"', '"')
            # Parse float values
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            # Parse integer values
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue

            setattr(new_instance, key, value)

        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance based on class name and id."""
        try:
            args = shlex.split(arg)
        except Exception:
            args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        objs = models.storage.all()
        if key in objs:
            print(objs[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        try:
            args = shlex.split(arg)
        except Exception:
            args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        objs = models.storage.all()
        if key in objs:
            del objs[key]
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances based or not on class name."""
        try:
            args = shlex.split(arg)
        except Exception:
            args = arg.split()
        objs = models.storage.all()
        list_instances = []
        if len(args) > 0:
            if args[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            for key, obj in objs.items():
                if key.split('.')[0] == args[0]:
                    list_instances.append(str(obj))
        else:
            for obj in objs.values():
                list_instances.append(str(obj))
        print(list_instances)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
