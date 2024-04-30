#!/usr/bin/python3
"""
Creates states route
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City

