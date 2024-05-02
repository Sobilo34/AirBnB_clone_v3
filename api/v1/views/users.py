
#!/usr/bin/python3
"""
Creates cities route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """ returns list of all users """
    users = storage.all(User)
    # returns the list of users
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ returns a user """
    user = storage.get(User, user_id)
    # returns 404 if user not found
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ deletes a user """
    user = storage.get(User, user_id)
    # returns 404 if user not found
    if not user:
        abort(404)
    # deletes the user
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ creates a user """
    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description='Missing email')
    if 'password' not in request.get_json():
        abort(400, description='Missing password')
    data = request.get_json()
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ updates a user """
    user = storage.get(User, user_id)
    # returns 404 if user not found
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore = ["id", "created_at", "updated_at", "email"]
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
