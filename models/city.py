#!/usr/bin/python3
"""Defines the City class."""
import os
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class City(BaseModel, Base):
    """Represents a city."""
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        places = relationship(
            'Place',
            backref='cities',
            cascade='all, delete-orphan'
        )
    else:
        @property
        def places(self):
            """Getter for FileStorage: Places located in this city."""
            return [p for p in models.storage.all("Place").values()
                    if p.city_id == self.id]
