"""The api submodule contains routes that dont render templates.
"""
from os import environ
from flask import Blueprint
from .api import api_routes

api = Blueprint("api", __name__, template_folder="templates",
                url_prefix="/api")

api.register_blueprint(api_routes)
