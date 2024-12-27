import time
from datetime import datetime

from flask import Blueprint, abort, redirect, render_template, request, url_for

from ....tools import formatDatetime
from .task import tasks_site

spielleitung_site = Blueprint(
    "spielleitung", __name__, url_prefix="/spielleitung")


spielleitung_site.register_blueprint(tasks_site)

# activate back button


@spielleitung_site.context_processor
def inject_back():
    return dict(backact=True)


@spielleitung_site.route("/")
def index():
    return render_template("spielleitung/index.html")
