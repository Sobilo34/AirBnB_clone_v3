#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        storage = models.storage
        self.assertIs(type(storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        storage = models.storage
        all_cls = storage.all()
        self.assertEqual(len(all_cls), storage.count())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        all_objs = models.storage.all()
        state = State(name="Nigeria")
        models.storage.new(state)
        session = models.storage._DBStorage__session
        query_state = session.query(State).filter_by(id=state.id).first()
        self.assertEqual(query_state.id, state.id)
        self.assertEqual(query_state.name, state.name)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        all_objs = models.storage.all()
        state = State(name="Nigeria")
        models.storage.new(state)
        models.storage.save()
        self.assertTrue(models.storage.count() > len(all_objs))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """ test that it returns an obj if id is provided """
        state = State(name="Gana")
        models.storage.new(state)
        models.storage.save()
        retrived_obj = models.storage.get(State, state.id)
        self.assertEqual(state.id, retrived_obj.id)
        self.assertEqual(state.name, retrived_obj.name)
        self.assertIsNone(models.storage.get("fake", state.id))
        self.assertIsNone(models.storage.get("State", "fake"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """  test case for storage.count """
        state = State(name="Gana")
        models.storage.new(state)
        models.storage.save()
        session = models.storage._DBStorage__session
        count_state = len(session.query(State).all())
        # count returns all instances of a class if class is provided
        self.assertEqual(count_state, models.storage.count(State))
        # count returns all if class is not provided
        count_all = len(models.storage.all())
        self.assertEqual(count_all, models.storage.count())
        # check if the returned count is a number
        self.assertTrue(type(models.storage.count()), int)
        self.assertTrue(type(models.storage.count(State)), int)
