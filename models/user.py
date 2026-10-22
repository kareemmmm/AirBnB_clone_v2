#!/usr/bin/python3
"""Defines the User class."""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class User(BaseModel, Base):
    """Represents a user."""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
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
    else:
        @property
        def places(self):
            """Getter for FileStorage: Places owned by this user."""
            return [p for p in models.storage.all("Place").values()
                    if p.user_id == self.id]

        @property
        def reviews(self):
            """Getter for FileStorage: Reviews written by this user."""
            return [r for r in models.storage.all("Review").values()
                    if r.user_id == self.id]
