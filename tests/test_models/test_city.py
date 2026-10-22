#!/usr/bin/python3
"""Unittests for models/city.py."""
import unittest
import os
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):
    """Test suite for the City class."""

    def tearDown(self):
        """Clean up temporary JSON files."""
        try:
            os.remove("file.json")
        except OSError:
            pass

    def test_is_subclass(self):
        """Test that City inherits from BaseModel."""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(issubclass(type(city), BaseModel))

    def test_default_attributes(self):
        """Test that columns start unset (None) until assigned."""
        city = City()
        self.assertIsNone(city.state_id)
        self.assertIsNone(city.name)

    def test_attribute_assignment(self):
        """Test attribute assignment."""
        city = City()
        city.state_id = "CA-123"
        city.name = "San Francisco"
        self.assertEqual(city.state_id, "CA-123")
        self.assertEqual(city.name, "San Francisco")

    def test_to_dict(self):
        """Test to_dict method with City attributes."""
        city = City()
        c_dict = city.to_dict()
        self.assertEqual(type(c_dict), dict)
        self.assertEqual(c_dict["__class__"], "City")


if __name__ == "__main__":
    unittest.main()
