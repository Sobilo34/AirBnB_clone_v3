#!/usr/bin/python3
"""
The view on amenitied
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"])
def get_amenities():

    """
    Retrieves all amenities.
    """
    amenities = storage.all(Amenity).values()
    amenities_list = []

    for ameni in amenities:
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """
    Retrieves a specific amenity by ID.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """
    Deletes an amenity by it ID
    """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """
    Creates a new amenity.
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    content = request.get_json()
    instance = Amenity(**content)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """
    Updates an amenity by it ID
    """
    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)

    data = request.get_json()

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
