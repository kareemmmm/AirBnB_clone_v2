#!/usr/bin/python3
"""Defines the User class."""
import hashlib
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

    def __init__(self, *args, **kwargs):
        """Initializes a User instance."""
        if kwargs and "password" in kwargs:
            pwd = kwargs["password"]
            if isinstance(pwd, str):
                kwargs["password"] = hashlib.md5(pwd.encode()).hexdigest()
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Sets an attribute, hashing the password if it's updated."""
        if name == "password" and isinstance(value, str):
            value = hashlib.md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
