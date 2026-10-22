#!/usr/bin/python3
"""Defines the BaseModel class."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime

try:
    from sqlalchemy.orm import declarative_base
except ImportError:  # SQLAlchemy < 1.4
    from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models."""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        now = datetime.utcnow()
        self.id = str(uuid.uuid4())
        self.created_at = now
        self.updated_at = now
        for key, value in kwargs.items():
            if key == "__class__":
                continue
            if key in ("created_at", "updated_at") and isinstance(value, str):
                value = datetime.fromisoformat(value)
            setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance."""
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """Updates updated_at with current time and saves to storage."""
        from models import storage
        self.updated_at = datetime.utcnow()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Converts the instance into a dictionary."""
        dictionary = {}
        for key, value in self.__dict__.items():
            if key == "_sa_instance_state":
                continue
            # skip loaded relationship objects (not JSON serializable)
            if isinstance(value, BaseModel):
                continue
            if isinstance(value, list) and any(
                    isinstance(v, BaseModel) for v in value):
                continue
            dictionary[key] = value
        dictionary["__class__"] = type(self).__name__
        if isinstance(self.created_at, datetime):
            dictionary["created_at"] = self.created_at.isoformat()
        if isinstance(self.updated_at, datetime):
            dictionary["updated_at"] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """Deletes the current instance from storage."""
        from models import storage
        storage.delete(self)
