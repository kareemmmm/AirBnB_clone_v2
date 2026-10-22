#!/usr/bin/python3
"""Unittests for models/engine/file_storage.py."""
import unittest
import os
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test suite for the FileStorage class."""

    def setUp(self):
        """Reset storage and clear existing json file."""
        FileStorage._FileStorage__objects = {}
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Clean up json file after testing."""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_all_returns_dict(self):
        """Test that all() returns a dictionary."""
        self.assertEqual(type(models.storage.all()), dict)

    def test_new(self):
        """Test that new() adds an object to __objects."""
        bm = BaseModel()
        models.storage.new(bm)
        key = "BaseModel.{}".format(bm.id)
        self.assertIn(key, models.storage.all())

    def test_save(self):
        """Test that save() writes objects to file.json."""
        bm = BaseModel()
        bm.save()
        self.assertTrue(os.path.exists("file.json"))

    def test_reload(self):
        """Test reload() restores saved objects from file.json."""
        bm = BaseModel()
        bm.save()
        models.storage.all().clear()
        models.storage.reload()
        key = "BaseModel.{}".format(bm.id)
        self.assertIn(key, models.storage.all())


if __name__ == "__main__":
    unittest.main()
