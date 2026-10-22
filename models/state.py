#!/usr/bin/python3
"""Defines the State class."""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    """Represents a state."""
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
            """Getter for FileStorage: Cities linked to this state."""
            return [c for c in models.storage.all(City).values()
                    if c.state_id == self.id]
