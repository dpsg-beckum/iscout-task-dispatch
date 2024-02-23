from .team import teams_site
from .task import tasks_site
from flask import render_template, request, abort, redirect, url_for
from ....database.handel import *
from ..tools import formatDatetime
from flask import Blueprint
import time
from datetime import datetime

spielleitung_site = Blueprint(
    "spielleitung_site", __name__, url_prefix="/spielleitung")


spielleitung_site.register_blueprint(tasks_site)
spielleitung_site.register_blueprint(teams_site)


@spielleitung_site.route("/")
def index():
    return render_template("spielleitung/index.html")
