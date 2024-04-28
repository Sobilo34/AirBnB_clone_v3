#!/usr/bin/python3
"""
THis is a python file
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """The status"""
    return jsonify({"status": "OK"})