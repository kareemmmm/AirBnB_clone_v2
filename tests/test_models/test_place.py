#!/usr/bin/python3
"""Unittests for models/place.py."""
import unittest
import os
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Test suite for the Place class."""

    def tearDown(self):
        """Clean up temporary JSON files."""
        try:
            os.remove("file.json")
        except OSError:
            pass

    def test_is_subclass(self):
        """Test that Place inherits from BaseModel."""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(issubclass(type(place), BaseModel))

    def test_default_attributes(self):
        """Test that columns start unset (None) until assigned."""
        place = Place()
        self.assertIsNone(place.city_id)
        self.assertIsNone(place.user_id)
        self.assertIsNone(place.name)
        self.assertIsNone(place.description)
        self.assertIsNone(place.latitude)
        self.assertIsNone(place.longitude)
        if os.getenv("HBNB_TYPE_STORAGE") != "db":
            self.assertEqual(place.amenity_ids, [])

    def test_attribute_types(self):
        """Test attribute type assignments."""
        place = Place(city_id="c1", user_id="u1", name="House",
                      description="Nice", number_rooms=2,
                      number_bathrooms=1, max_guest=4, price_by_night=100,
                      latitude=1.5, longitude=2.5)
        self.assertIsInstance(place.city_id, str)
        self.assertIsInstance(place.user_id, str)
        self.assertIsInstance(place.name, str)
        self.assertIsInstance(place.description, str)
        self.assertIsInstance(place.number_rooms, int)
        self.assertIsInstance(place.number_bathrooms, int)
        self.assertIsInstance(place.max_guest, int)
        self.assertIsInstance(place.price_by_night, int)
        self.assertIsInstance(place.latitude, float)
        self.assertIsInstance(place.longitude, float)
        if os.getenv("HBNB_TYPE_STORAGE") != "db":
            self.assertIsInstance(place.amenity_ids, list)

    def test_to_dict(self):
        """Test to_dict method with Place attributes."""
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(type(place_dict), dict)
        self.assertEqual(place_dict["__class__"], "Place")
        self.assertIn("id", place_dict)
        self.assertIn("created_at", place_dict)
        self.assertIn("updated_at", place_dict)


if __name__ == "__main__":
    unittest.main()
