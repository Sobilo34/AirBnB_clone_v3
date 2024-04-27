#!/usr/bin/python3
"""
"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """ Closes database"""
    storage.close()


if __name__== "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"), port=os.getenv("HBNB_API_PORT", 5000), threaded=True)
