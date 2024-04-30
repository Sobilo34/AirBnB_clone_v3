#!/usr/bin/python3
"""
Creates states route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ returns list of all cities of a state """
    state = storage.get(State, state_id)
    # return 404 if state not found
    if not state:
        abort(404)
    # returns the list of cities of a state if the state exists
    city_list = [city.to_dict() for city in state.cities]
    return make_response(jsonify(city_list), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ returns list of all cities of a state """
    city = storage.get(City, city_id)
    # return 404 if state not found
    if not city:
        abort(404)
    return make_response(jsonify(city.to_dict()), 200)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ return a state with a given id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)
