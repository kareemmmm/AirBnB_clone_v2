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
    """Handles storage in a MySQL database with SQLAlchemy."""
    __engine = None
    __session = None
    __classes = {
        "State": State,
        "City": City,
        "User": User,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def __init__(self):
        """Creates the engine from the HBNB_MYSQL_* environment variables."""
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
        """Queries the current session for all objects (or of one class).

        cls can be a class or a class name (string).
        """
        if isinstance(cls, str):
            cls = DBStorage.__classes.get(cls)
            if cls is None:
                return {}
        classes = [cls] if cls is not None else DBStorage.__classes.values()
        obj_dict = {}
        for c in classes:
            if c not in DBStorage.__classes.values():
                continue
            for obj in self.__session.query(c).all():
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Adds the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session if not None."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables and a new thread-safe session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Closes the current session (calls remove())."""
        self.__session.remove()
