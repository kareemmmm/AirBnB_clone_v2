#!/usr/bin/python3
"""Defines the Amenity class."""
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Represents an amenity for a MySQL database."""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
