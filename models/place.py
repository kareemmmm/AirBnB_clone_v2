#!/usr/init/python3
#!/usr/bin/python3
"""Defines the Place class."""
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.review import Review
import models

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False
        ),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False
        )
    )


class Place(BaseModel, Base):
    """Represents a place for a MySQL database."""
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
            secondary='place_amenity',
            viewonly=False,
            backref='place_amenities'
        )
    else:
        amenity_ids = []

        def __init__(self, *args, **kwargs):
            """Initializes Place instance."""
            super().__init__(*args, **kwargs)
            if not hasattr(self, 'amenity_ids'):
                self.amenity_ids = []

        @property
        def reviews(self):
            """Getter attribute for FileStorage relationship with Review."""
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Getter attribute for amenities in FileStorage."""
            from models.amenity import Amenity
            amenity_list = []
            for amenity_id in self.amenity_ids:
                amenity = models.storage.all().get("Amenity." + amenity_id)
                if amenity:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            """Setter attribute for amenities in FileStorage."""
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
