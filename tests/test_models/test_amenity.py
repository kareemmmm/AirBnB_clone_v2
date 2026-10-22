#!/usr/bin/python3
"""Unittests for models/amenity.py."""
import unittest
import os
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Test suite for the Amenity class."""

    def tearDown(self):
        """Clean up temporary JSON files."""
        try:
            os.remove("file.json")
        except OSError:
            pass

    def test_is_subclass(self):
        """Test that Amenity inherits from BaseModel."""
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(issubclass(type(amenity), BaseModel))

    def test_default_attributes(self):
        """Test that columns start unset (None) until assigned."""
        amenity = Amenity()
        self.assertIsNone(amenity.name)

    def test_to_dict(self):
        """Test to_dict method with Amenity attributes."""
        amenity = Amenity()
        a_dict = amenity.to_dict()
        self.assertEqual(type(a_dict), dict)
        self.assertEqual(a_dict["__class__"], "Amenity")


if __name__ == "__main__":
    unittest.main()
