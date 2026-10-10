cat << 'EOF' > tests/test_models/test_engine/test_db_storage.py
#!/usr/bin/python3
"""Contains the TestDBStorage classes."""
unittest = __import__('unittest')
State = __import__('models.state').state.State
DBStorage = __import__('models.engine.db_storage').db_storage.DBStorage
os = __import__('os')


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class."""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not testing DBStorage")
    def test_all_class(self):
        """Test that all returns database objects."""
        storage = DBStorage()
        storage.reload()
        state = State(name="Cairo")
        storage.new(state)
        storage.save()
        objs = storage.all(State)
        self.assertIn("State." + state.id, objs)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Not testing DBStorage")
    def test_new(self):
        """Test that new adds an object to the session."""
        storage = DBStorage()
        storage.reload()
        state = State(name="Giza")
        storage.new(state)
        self.assertIn(state, storage._DBStorage__session.new)
EOF
