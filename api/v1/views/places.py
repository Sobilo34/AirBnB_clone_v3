#!/usr/bin/python3
"""
Creates cities route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ returns list of all places in a city """
    city = storage.get(City, city_id)
    # return 404 if state not found
    if not city:
        abort(404)
    # returns the list of cities of a state if the state exists
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ returns list of a place in a city """
    place = storage.get(Place, place_id)
    # return 404 if place not found
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(place_id):
    """ return a state with a given id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)
