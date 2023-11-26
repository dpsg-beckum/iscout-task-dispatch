from flask import Blueprint, render_template
from .views import task_views, team_views, overview
from ..sockets.socket_setup import socketio

site = Blueprint("site", __name__, template_folder="templates")


site.register_blueprint(task_views.tasks_site)
site.register_blueprint(team_views.teams_site)
site.register_blueprint(overview.overview_site)


@site.route("/")
def index():
    return render_template("index.html")