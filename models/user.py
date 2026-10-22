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
