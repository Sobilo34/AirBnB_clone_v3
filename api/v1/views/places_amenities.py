#!/usr/bin/python3
"""
Endpoints for managing amenities associated with places.
"""

from os import environ
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flasgger.utils import swag_from
from flask import abort, jsonify, make_response, request


@app_views.route("/places/<place_id>/amenities")
def get_place_amenities(place_id):

    """
    Retrieve all amenities associated with a specific place.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]

    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """
    Delete an amenity associated with a specific place.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)

    else:
        if amenity_id not in place.amenity_ids:
            abort(404)

        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def update_place_amenity(place_id, amenity_id):
    """
    Update the amenities associated with a specific place.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)

        else:
            place.amenities.append(amenity)

    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)

        else:
            place.amenity_ids.append(amenity_id)

    storage.save()

    return make_response(jsonify(amenity.to_dict()), 201)
