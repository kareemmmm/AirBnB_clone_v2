#!/usr/bin/python3
"""Unittests for models/state.py."""
import unittest
import os
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Test suite for the State class."""

    def tearDown(self):
        """Clean up temporary JSON files."""
        try:
            os.remove("file.json")
        except OSError:
            pass

    def test_is_subclass(self):
        """Test that State inherits from BaseModel."""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(issubclass(type(state), BaseModel))

    def test_default_attributes(self):
        """Test that columns start unset (None) until assigned."""
        state = State()
        self.assertIsNone(state.name)

    def test_attribute_assignment(self):
        """Test attribute assignment."""
        state = State()
        state.name = "California"
        self.assertEqual(state.name, "California")

    def test_to_dict(self):
        """Test to_dict method with State attributes."""
        state = State()
        s_dict = state.to_dict()
        self.assertEqual(type(s_dict), dict)
        self.assertEqual(s_dict["__class__"], "State")
        self.assertIn("id", s_dict)


if __name__ == "__main__":
    unittest.main()
