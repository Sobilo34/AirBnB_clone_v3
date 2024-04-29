#!/usr/bin/python3
"""
THis is a python file
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """The status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ returns the status of the data in the database """
    clss = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    response = {}
    for key, value in clss.items():
        response[key] = storage.count(value)
    # response = {
    #     "amenities": storage.count("Amenity"),
    #     "cities": storage.count("City"),
    #     "places": storage.count("Place"),
    #     "reviews": storage.count("Review"),
    #     "states": storage.count("State"),
    #     "users": storage.count("User")
    # }
    return jsonify(response)
