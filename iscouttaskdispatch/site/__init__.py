from flask import Blueprint, render_template

from .views import spielleitung
from .views import overview
from .views import player

site = Blueprint("site", __name__, template_folder="templates/")


site.register_blueprint(spielleitung.spielleitung_site)
site.register_blueprint(player.player_site)
site.register_blueprint(overview.overview_site)


@site.route("/")
def index():
    return render_template("index.html")