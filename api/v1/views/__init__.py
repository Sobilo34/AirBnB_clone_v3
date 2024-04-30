#!/usr/bin/python3
"""
This is to initialize the packages
"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *  # nopep8
from api.v1.views.states import *  # nopep8
