#!/usr/bin/python3
"""
Creates states route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ returns list of all cities of a state """
    state = storage.get(State, state_id)
    # return 404 if state not found
    if not state:
        abort(404)
    # returns the list of cities of a state if the state exists
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)