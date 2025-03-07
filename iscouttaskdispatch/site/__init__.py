from flask import Blueprint, redirect, render_template, session, url_for

from ..database.db import Team
from ..database.exceptions import ElementDoesNotExsist
from .views import overview, spielleitung, team

site = Blueprint("site", __name__, template_folder="templates")


site.register_blueprint(spielleitung.spielleitung_site)
site.register_blueprint(team.teams_site)
site.register_blueprint(overview.overview_site)


@site.errorhandler(ElementDoesNotExsist)
def handle_element_does_not_exist(error):
    return render_template("error.html", error=error, code=404), 404


@site.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@site.context_processor
def inject_teams():
    session["refresh"] = session.get("refresh", True)
    session["refresh_interval"] = 20
    session["translate"] = session.get("translate", False)
    data = {}
    data["teams"] = [t.to_dict() for t in Team.get_all()]
    return data


@site.route("/")
def index():
    return render_template("index.html")


@site.route("/togglerefresh")
def togglerefresh():
    session["refresh"] = not session.get("refresh", False)
    return redirect(url_for("site.index"))


@site.route("/toggletranslate")
def toggletranslate():
    session["translate"] = not session.get("translate", False)
    return redirect(url_for("site.index"))
