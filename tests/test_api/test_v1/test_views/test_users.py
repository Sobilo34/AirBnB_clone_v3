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
from flask import Flask
from api.v1.views import app_views
from models import storage
from models.user import User


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


class TestUsersRoute(unittest.TestCase):
    def setUp(self):
        """Set up the test app"""
        self.app = Flask(__name__)
        self.app.register_blueprint(app_views)
        self.client = self.app.test_client()
        self.user = User(
            last_name="dennis",
            first_name="chiedu",
            email="dennis@yahoo.com",
            password="asdfjkl;"
        )
        self.user.save()

    def tearDown(self):
        """Clean up after the test"""
        # Clean up any test data here

    def test_get_users(self):
        """Test GET /users route"""
        response = self.client.get('/api/v1/users')
        # checks the status code
        self.assertEqual(response.status_code, 200)
        # Check if content type is JSON
        self.assertEqual(response.content_type, 'application/json')
        # Get response data as JSON
        json_data = response.json
        # Assert that JSON data is a list
        self.assertTrue(isinstance(json_data, list))

    def test_get_user(self):
        """Test GET /users/<user_id> route"""
        response = self.client.get('/api/v1/users/{}'.format(self.user.id))
        # checks the status code
        self.assertEqual(response.status_code, 200)
        # Check if content type is JSON
        self.assertEqual(response.content_type, 'application/json')
        # Get response data as JSON
        json_data = response.json
        # Assert that JSON data is a list
        self.assertTrue(isinstance(json_data, dict))
        self.assertEqual(json_data, self.user.to_dict())

    def test_delete_user(self):
        """Test GET /users/<user_id> route"""
        self.user.save()
        response = self.client.delete(f'/api/v1/users/{self.user.id}')
        # checks the status code
        self.assertEqual(response.status_code, 200)
        # Check if content type is JSON
        self.assertEqual(response.content_type, 'application/json')
        # Get response data as JSON
        json_data = response.json
        # Assert that JSON data is a list
        self.assertTrue(isinstance(json_data, dict))
        # compare that it returns empty response
        self.assertEqual(json_data, {})
        # request for the deleted user and test that it does not exist
        response = self.client.delete(f'/api/v1/users/{self.user.id}')
        # checks the status code is 404 (not found)
        self.assertEqual(response.status_code, 404)
