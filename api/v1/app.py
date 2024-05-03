#!/usr/bin/python3
"""
An API application
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}}))


@app.teardown_appcontext
def teardown(exception):
    """ Closes database"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handle error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    """
    set the defaults
    """
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
