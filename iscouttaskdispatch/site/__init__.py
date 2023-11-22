from flask import Blueprint, render_template
from .views import task_views, team_views


site = Blueprint("site", __name__, template_folder="templates")


# Register task views
site.register_blueprint(task_views.tasks_site)
# Register team views
site.register_blueprint(team_views.teams_site)


@site.route("/")
def index():
    return render_template("index.html")