#!/usr/bin/python3
"""Contains the TestDBStorage class (runs only when HBNB_TYPE_STORAGE=db)."""
import os
import unittest
from models.state import State


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Not testing DBStorage")
class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class."""

    def setUp(self):
        """Use the storage instance created by the models package."""
        import models
        self.storage = models.storage

    def test_all_class(self):
        """Test that all() returns objects of the requested class."""
        state = State(name="Cairo")
        state.save()
        objs = self.storage.all(State)
        self.assertIn("State." + state.id, objs)

    def test_all_class_name(self):
        """Test that all() also accepts the class name as a string."""
        state = State(name="Alexandria")
        state.save()
        self.assertIn("State." + state.id, self.storage.all("State"))

    def test_new(self):
        """Test that new() adds an object to the session."""
        state = State(name="Giza")
        self.storage.new(state)
        self.assertIn(state, self.storage._DBStorage__session.new)
        self.storage.save()

    def test_delete(self):
        """Test that delete() removes an object after save()."""
        state = State(name="Luxor")
        state.save()
        self.storage.delete(state)
        self.storage.save()
        self.assertNotIn("State." + state.id, self.storage.all(State))


if __name__ == "__main__":
    unittest.main()
