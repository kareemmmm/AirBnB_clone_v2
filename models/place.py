#!/usr/bin/python3
"""Defines the Place class."""
import os
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.review import Review
import models


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
    else:
        @property
        def reviews(self):
            """Getter attribute for FileStorage relationship with Review."""
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list
