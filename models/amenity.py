#!/usr/bin/python3
"""Defines the Amenity class."""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Represents an Amenity for a MySQL database."""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = relationship(
            'Place',
            secondary='place_amenity',
            backref='amenities'
        )
