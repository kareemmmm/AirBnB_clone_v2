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
            self.save()

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
