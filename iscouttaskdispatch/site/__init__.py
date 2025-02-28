from flask import Blueprint, render_template

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
    data = {}
    data["teams"] = [t.to_dict() for t in Team.get_all()]
    return data


@site.route("/")
def index():
    return render_template("index.html")
