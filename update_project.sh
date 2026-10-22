#!/bin/bash
# Script to update all core models and engine files for DBStorage / AirBnB_clone_v2

echo "Updating models/base_model.py..."
cat << 'BASEMODEL' > models/base_model.py
#!/usr/bin/python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models."""
    __abstract__ = True
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    if isinstance(value, str):
                        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """Returns a string representation of the instance."""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """Updates updated_at with current time and saves to storage."""
        self.updated_at = datetime.utcnow()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format."""
        dictionary = self.__dict__.copy()
        dictionary["__class__"] = type(self).__name__
        if isinstance(self.created_at, datetime):
            dictionary["created_at"] = self.created_at.isoformat()
        if isinstance(self.updated_at, datetime):
            dictionary["updated_at"] = self.updated_at.isoformat()
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        """Deletes the current instance from storage."""
        from models import storage
        storage.delete(self)
BASEMODEL

echo "Updating models/city.py..."
cat << 'CITY' > models/city.py
#!/usr/bin/python3
"""Defines the City class."""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """Represents a city for a MySQL database."""
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
CITY

echo "Updating models/state.py..."
cat << 'STATE' > models/state.py
#!/usr/bin/python3
"""Defines the State class."""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    """Represents a state for a MySQL database."""
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            'City',
            backref='state',
            cascade='all, delete-orphan'
        )
    else:
        @property
        def cities(self):
            """Getter attribute for FileStorage relationship with City."""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
STATE

echo "Updating models/user.py..."
cat << 'USER' > models/user.py
#!/usr/bin/python3
"""Defines the User class."""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Represents a user for a MySQL database."""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship(
        'Place',
        backref='user',
        cascade='all, delete-orphan'
    )
    reviews = relationship(
        'Review',
        backref='user',
        cascade='all, delete-orphan'
    )
USER

echo "Updating models/place.py..."
cat << 'PLACE' > models/place.py
#!/usr/bin/python3
"""Defines the Place class."""
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from models.base_model import BaseModel, Base


class Place(BaseModel, Base):
    """Represents a place for a MySQL database."""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
PLACE

echo "Updating models/amenity.py..."
cat << 'AMENITY' > models/amenity.py
#!/usr/bin/python3
"""Defines the Amenity class."""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Represents an amenity for a MySQL database."""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
AMENITY

echo "Updating models/review.py..."
cat << 'REVIEW' > models/review.py
#!/usr/bin/python3
"""Defines the Review class."""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """Represents a review for a MySQL database."""
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
REVIEW

echo "Updating models/engine/db_storage.py..."
cat << 'DBSTORAGE' > models/engine/db_storage.py
#!/usr/bin/python3
"""Defines the DBStorage class."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Handles SQLAlchemy database storage."""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage engine."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db),
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects."""
        obj_dict = {}
        classes = {
            "State": State,
            "City": City,
            "User": User,
            "Place": Place,
            "Amenity": Amenity,
            "Review": Review
        }

        if cls:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls:
                query = self.__session.query(cls)
                for obj in query.all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
        else:
            for c in classes.values():
                query = self.__session.query(c)
                for obj in query.all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize session."""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """Call remove() on private session attribute."""
        self.__session.remove()
DBSTORAGE

echo "Updating models/__init__.py..."
cat << 'INIT' > models/__init__.py
#!/usr/bin/python3
"""Instantiates a storage object depending on environment variable."""
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
INIT

chmod +x update_project.sh
./update_project.sh
echo "All project files updated successfully!"
