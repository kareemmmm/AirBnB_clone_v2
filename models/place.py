#!/usr/bin/python3
"""Defines the Place class and the place_amenity link table."""
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models

# Many-to-many link table between places and amenities (PlaceAmenity)
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """Represents a place."""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship(
            'Review',
            backref='place',
            cascade='all, delete-orphan'
        )
        amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            back_populates='place_amenities',
            viewonly=False
        )
    else:
        def __init__(self, *args, **kwargs):
            """Initializes a Place (FileStorage keeps amenity ids)."""
            super().__init__(*args, **kwargs)
            if "amenity_ids" not in kwargs:
                self.amenity_ids = []

        @property
        def reviews(self):
            """Getter for FileStorage: Reviews of this place."""
            return [r for r in models.storage.all("Review").values()
                    if r.place_id == self.id]

        @property
        def amenities(self):
            """Getter for FileStorage: Amenities linked to this place."""
            return [a for a in models.storage.all("Amenity").values()
                    if a.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter for FileStorage: links an Amenity to this place."""
            if type(obj).__name__ == "Amenity":
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
