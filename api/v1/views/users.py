#!/usr/bin/python3
"""
Creates cities route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"])
def get_users():

    """
    Retrieve all users.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return make_response(jsonify(users), 200)


@app_views.route("/users/<string:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Retrieve a specific user by ID.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return make_response(jsonify(user.to_dict()), 200)


@app_views.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user by ID.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"])
def create_user():
    """
    Create a new user.
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update a user by ID.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for attr, val in data.items():
        if attr not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, attr, val)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
