-- Prepares a MySQL server for the development environment (hbnb_dev_db)
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db. TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
EOF   

echo "[] Writing setup_mysql_test.sql..."
cat << 'EOF' > setup_mysql_test.sql
-- Prepares a MySQL server for the test environment (hbnb_test_db)
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db. TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
EOF   

echo "[*] Updating models/engine/file_storage.py..."
cat << 'EOF' > models/engine/file_storage.py
#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
"""Serializes instances to a JSON file and deserializes JSON file to instances."""
__file_path = "file.json"
__objects = {}

def all(self, cls=None):
    """Returns the list of objects of one type of class if cls is given."""
    if cls is not None:
        filtered_dict = {}
        for key, val in FileStorage.__objects.items():
            if cls == val.__class__ or cls == val.__class__.__name__:
                filtered_dict[key] = val
        return filtered_dict
    return FileStorage.__objects

def new(self, obj):
    """Sets in __objects the obj with key <obj class name>.id."""
    key = "{}.{}".format(obj.__class__.__name__, obj.id)
    FileStorage.__objects[key] = obj

def save(self):
    """Serializes __objects to the JSON file (path: __file_path)."""
    obj_dict = {
        key: obj.to_dict() for key, obj in FileStorage.__objects.items()
    }
    with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
        json.dump(obj_dict, f)

def reload(self):
    """Deserializes the JSON file to __objects (if path exists)."""
    try:
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            obj_dict = json.load(f)
            for key, val in obj_dict.items():
                class_name = val["__class__"]
                if hasattr(models, class_name):
                    cls = getattr(models, class_name)
                    FileStorage.__objects[key] = cls(**val)
    except FileNotFoundError:
        pass

def delete(self, obj=None):
    """Deletes obj from __objects if it exists."""
    if obj is not None:
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
            self.save()
