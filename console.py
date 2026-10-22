#!/usr/bin/python3
"""Defines the HBNBCommand console interpreter."""
import ast
import cmd
import re
import shlex
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

# matches key="quoted value" or key=unquoted_value
PARAM_RE = re.compile(r'(\w+)=("(?:[^"\\]|\\.)*"|\S+)')


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

    @staticmethod
    def _split(arg):
        """Splits a command line into arguments (quote aware)."""
        try:
            return shlex.split(arg)
        except ValueError:
            return arg.split()

    @staticmethod
    def _parse_params(text):
        """Parses key=value pairs of the create command.

        Strings: "value" ('_' becomes a space, \\" becomes ").
        Floats: 3.14   Integers: 42   Anything else is skipped.
        """
        params = {}
        for key, value in PARAM_RE.findall(text):
            if key in ("__class__",):
                continue
            if value.startswith('"'):
                if len(value) < 2 or not value.endswith('"'):
                    continue
                value = value[1:-1].replace('\\"', '"').replace('_', ' ')
            elif re.fullmatch(r'-?\d+', value):
                value = int(value)
            elif re.fullmatch(r'-?\d+\.\d+', value):
                value = float(value)
            else:
                continue
            params[key] = value
        return params

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
        """Creates a new instance: create <Class> <key>=<value> ..."""
        parts = arg.split(None, 1)
        if not parts:
            print("** class name missing **")
            return
        if parts[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        params = self._parse_params(parts[1] if len(parts) > 1 else "")
        new_instance = HBNBCommand.__classes[parts[0]](**params)
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints an instance: show <Class> <id>"""
        args = self._split(arg)
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
        """Deletes an instance: destroy <Class> <id>"""
        args = self._split(arg)
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
            models.storage.delete(objs[key])
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all instances, or all of one class: all [<Class>]"""
        args = self._split(arg)
        objs = models.storage.all()
        if len(args) > 0:
            if args[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            result = [str(obj) for key, obj in objs.items()
                      if key.split('.')[0] == args[0]]
        else:
            result = [str(obj) for obj in objs.values()]
        print(result)

    def do_count(self, arg):
        """Prints the number of instances of a class: count <Class>"""
        args = self._split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        objs = models.storage.all()
        print(len([k for k in objs if k.split('.')[0] == args[0]]))

    def do_update(self, arg):
        """Updates an instance: update <Class> <id> <attribute> <value>"""
        args = self._split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        objs = models.storage.all()
        key = "{}.{}".format(args[0], args[1])
        if key not in objs:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr, value = args[2], args[3]
        if attr in ("id", "created_at", "updated_at"):
            return
        if re.fullmatch(r'-?\d+', value):
            value = int(value)
        elif re.fullmatch(r'-?\d+\.\d+', value):
            value = float(value)
        obj = objs[key]
        setattr(obj, attr, value)
        obj.save()

    def default(self, line):
        """Handles <Class>.all(), .count(), .show(id), .destroy(id),
        .update(id, attr, value) and .update(id, {dict})."""
        match = re.fullmatch(r'(\w+)\.(\w+)\((.*)\)', line.strip())
        if not match:
            print("*** Unknown syntax: {}".format(line))
            return
        cls_name, method, inner = match.groups()
        try:
            params = ast.literal_eval("(" + inner + ",)") if inner else ()
        except (ValueError, SyntaxError):
            print("*** Unknown syntax: {}".format(line))
            return
        if method in ("all", "count") and not params:
            getattr(self, "do_" + method)(cls_name)
        elif method in ("show", "destroy") and len(params) == 1:
            getattr(self, "do_" + method)(
                "{} {}".format(cls_name, shlex.quote(str(params[0]))))
        elif method == "update" and len(params) == 2 and \
                isinstance(params[1], dict):
            for k, v in params[1].items():
                self.do_update("{} {} {} {}".format(
                    cls_name, shlex.quote(str(params[0])),
                    shlex.quote(str(k)), shlex.quote(str(v))))
        elif method == "update" and len(params) >= 1:
            self.do_update(" ".join(
                [cls_name] + [shlex.quote(str(p)) for p in params]))
        else:
            print("*** Unknown syntax: {}".format(line))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
