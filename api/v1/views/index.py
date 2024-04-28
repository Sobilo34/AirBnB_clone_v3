#!/usr/bin/python3
"""
THis is a python file
"""
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """The status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """ returns the status of the data in the database """
    response = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(response)