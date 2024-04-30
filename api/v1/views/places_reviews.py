#!/usr/bin/python3
"""
Creates cities route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.Review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ returns list of all review of a place """
    place = storage.get(Place, place_id)
    # return 404 if state not found
    if not place:
        abort(404)
    # returns the list of cities of a state if the state exists
    place_list = [place.to_dict() for place in place.reviews]
    return jsonify(place_list)


@app_views.route('/reviews/<review_id>>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ returns a review """
    review = storage.get(Review, review_id)
    # return 404 if review not found
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>>', methods=['DELETE'], strict_slashes=False)
def get_review(review_id):
    """ deletes a review """
    review = storage.get(Review, review_id)
    # return 404 if review not found
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ create review for a place """
    place = storage.get(Place, place_id)
    # return 404 if state not found
    if not place:
        abort(404)
    
