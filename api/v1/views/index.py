#!/usr/bin/python3
"""
creates a flask route that returns the status and stats of the app
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """The status"""
    return jsonify("status": "OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ returns the status of the data in the database """
    _response = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(_response)
