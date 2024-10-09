import time
from datetime import datetime

from flask import Blueprint, abort, redirect, render_template, request, url_for

from ....tools import formatDatetime
from .task import tasks_site
from .team import teams_site

spielleitung_site = Blueprint(
    "spielleitung_site", __name__, url_prefix="/spielleitung")


spielleitung_site.register_blueprint(tasks_site)
spielleitung_site.register_blueprint(teams_site)


@spielleitung_site.route("/")
def index():
    return render_template("spielleitung/index.html")
