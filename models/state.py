#!/usr/bin/python3
"""Defines the State class."""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.city import City
import models


class State(BaseModel, Base):
    """Represents a state for a MySQL database."""
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
            """Getter attribute for FileStorage relationship with City."""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
