#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

from datetime import datetime
import inspect
from api.v1.views import users
from models.base_model import BaseModel
import pep8
import unittest


class TestUsersDocs(unittest.TestCase):
    """Tests to check the documentation and style of users route"""
    users_f = inspect.getmembers(users, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Test that api/v1/views/users.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        """Test that tests/test_api/v1/views/test_users.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        f_path = ['tests/test_api/test_v1/test_views/test_users.py']
        result = pep8s.check_files(f_path)
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_users_module_docstring(self):
        """Test for the users.py module docstring"""
        self.assertIsNot(users.__doc__, None,
                         "usesr.py needs a docstring")
        self.assertTrue(len(users.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for func in self.users_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))
