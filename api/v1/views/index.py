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


@app_views.route('/api/v1/stats', strict_slashes=False)
def stats():
    """ returns the status of the data in the database """
    class_list = [Amenity, City, State, Place, Review, User]
    names = ["amenities", "cities", "states", "places", "reviews", "users"]
    response = {}

    for name, cls in zip(names, class_list):
        response[name] = storage.count(cls=cls)
    return response
    