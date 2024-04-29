#!/usr/bin/python3
"""
API routes for managing states.
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request


@app_views.route("/states", methods=["GET"])
def get_states():

    """
    Retrieve all states.
    """
    states_list = storage.all(State).values()
    list_of_states = []

    for state in states_list:
        list_of_states.append(state.to_dict())

    return jsonify(list_of_states)


@app_views.route("/states/<string:state_id>", methods=["GET"])
def get_state(state_id):

    """
    Retrieve a specific state by ID.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Delete a state by ID.
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"])
def create_state():
    """
    Create a new state.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def update_state(state_id):
    """
    Update an existing state.
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()

    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)