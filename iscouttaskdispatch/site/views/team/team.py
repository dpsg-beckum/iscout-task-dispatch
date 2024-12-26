import time
from datetime import datetime
from pprint import pprint

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)

from ....database.db import Task, Team
from ....tools import formatDatetime
from ...forms import NewTeamForm

id_site = Blueprint("id", __name__, url_prefix="/<int:id>")


@id_site.before_request
def load_team():
    """Load team into `g` before handling any request."""
    team: Team = Team.get_via_id(request.view_args.get('id'))
    if not team:
        abort(404, "Team not found")
    g.team = team


@id_site.context_processor
def inject_team():
    team: Team = g.team
    return {'team': team.to_dict()}


@id_site.route("/", methods=["GET", "POST"])
def redirect_overview(id):
    return redirect(url_for(".team", id=id))


@id_site.route("/overview", methods=["GET", "POST"])
def overview(id):
    team: Team = g.team

    assigned_tasks = [t for t in team.tasks
                      if t.team_id == team.id
                      and t.status_id == 2]

    failed_tasks = [t for t in team.tasks
                    if t.team_id == team.id
                    and t.status_id == 4]

    return render_template("team/overview.html",
                           assigned_tasks=[t.to_dict()
                                           for t in assigned_tasks],
                           failed_tasks=[t.to_dict() for t in failed_tasks])


@id_site.route("/tasks", methods=["GET", "POST"])
def tasks(id):
    team: Team = g.team

    if request.method == "POST":
        task_id = request.form.get("task_id")

        task = Task.get_via_id(task_id)
        try:
            task.assign_to_team(team)
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for(".tasks", id=id))
        return redirect(url_for(".overview", id=id))

    tasks = Task.get_unassigned_tasks()

    return render_template("team/tasks.html",
                           tasks=[t.to_dict() for t in tasks])
