#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Serializes instances to a JSON file and deserializes them back."""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary of __objects, optionally filtered by class.

        cls can be a class or a class name (string).
        """
        if cls is None:
            return FileStorage.__objects
        if isinstance(cls, str):
            cls = {"BaseModel": BaseModel, "User": User, "State": State,
                   "City": City, "Amenity": Amenity, "Place": Place,
                   "Review": Review}.get(cls)
            if cls is None:
                return {}
        return {key: obj for key, obj in FileStorage.__objects.items()
                if type(obj) is cls}

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (__file_path)."""
        serialized = {key: obj.to_dict()
                      for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists."""
        classes = {"BaseModel": BaseModel, "User": User, "State": State,
                   "City": City, "Amenity": Amenity, "Place": Place,
                   "Review": Review}
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
        except (FileNotFoundError, ValueError):
            return
        for key, val in obj_dict.items():
            cls = classes.get(val.get("__class__"))
            if cls is not None:
                FileStorage.__objects[key] = cls(**val)

    def delete(self, obj=None):
        """Deletes obj from __objects if it exists inside it."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
                self.save()

    def close(self):
        """Calls reload() to refresh the objects from the file."""
        self.reload()
