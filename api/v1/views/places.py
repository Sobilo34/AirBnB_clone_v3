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
def delete_place(place_id):
    """ return a state with a given id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ creates a place in a city """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ updates a place """
    place = storage.get(Place, place_id)
    # returns 404 if place not found
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
