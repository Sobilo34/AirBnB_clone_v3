#!/usr/bin/python3
"""
Creates cities route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """ returns list of all users """
    users = storage.all(User)
    # returns the list of users
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route('/users/user_id', methods=['GET'],
                 strict_slashes=False)
def get_user():
    """ returns a user """
    user = storage.get(User, user_id)
    # returns 404 if user not found
    if not user:
        abort(404)
    return jsonify(user.jsonify)


@app_views.route('/users/user_id', methods=['DELETE'],
                 strict_slashes=False)
def get_user():
    """ deletes a user """
    user = storage.get(User, user_id)
    # returns 404 if user not found
    if not user:
        abort(404)
    # deletes the user
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)
