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
    """Serializes instances to a JSON file and deserializes back to instances."""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary of __objects, optionally filtered by class."""
        if cls is not None:
            filtered_dict = {}
            for key, value in FileStorage.__objects.items():
                if isinstance(cls, str):
                    if key.split('.')[0] == cls:
                        filtered_dict[key] = value
                elif type(value) is cls:
                    filtered_dict[key] = value
            return filtered_dict
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (__file_path)."""
        serialized_objs = {}
        for key, obj in FileStorage.__objects.items():
            serialized_objs[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(serialized_objs, f)

    def reload(self):
        """Deserializes the JSON file to __objects if it exists."""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                obj_dict = json.load(f)
                for key, val in obj_dict.items():
                    class_name = val["__class__"]
                    if class_name in globals():
                        cls = globals()[class_name]
                        FileStorage.__objects[key] = cls(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects if it exists inside it."""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
                self.save()
