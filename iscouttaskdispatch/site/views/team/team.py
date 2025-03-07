from flask import Blueprint, flash, redirect, render_template, request, url_for

from ....database.db import Task, Team

id_site = Blueprint("id", __name__, url_prefix="/<int:id>")


@id_site.route("/", methods=["GET", "POST"])
def redirect_overview(id):
    return redirect(url_for(".overview", id=id))


@id_site.route("/overview", methods=["GET", "POST"])
def overview(id):
    team: Team = Team.get_via_id(id)

    assigned_tasks = [t for t in team.tasks
                      if t.team_id == team.id
                      and t.status_id == 2]

    failed_tasks = [t for t in team.tasks
                    if t.team_id == team.id
                    and t.status_id == 4]

    return render_template("team/overview.html",
                           team=team.to_dict(),
                           assigned_tasks=[t.to_dict()
                                           for t in assigned_tasks],
                           failed_tasks=[t.to_dict() for t in failed_tasks])


@id_site.route("/tasks", methods=["GET", "POST"])
def tasks(id):
    team: Team = Team.get_via_id(id)

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
                           team=team.to_dict(),
                           tasks=[t.to_dict() for t in tasks])
