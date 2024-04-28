#!/usr/bin/python3
"""
Creates states route
"""
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id=None):
    """ returns list of all state """
    
    states = storage.all(State)
    if states is None:
        abort(404)
    state_list = [value.to_dict() for value in states.values()]
    return jsonify(state_list), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ creates a state """
    
