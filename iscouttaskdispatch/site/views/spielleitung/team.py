from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from ....database.db import Status, Task, Team
from ....database.exceptions import ElementAlreadyExists, ElementDoesNotExsist
from ....tools import formatDatetime
from ...forms import EditTeamForm

teams_site = Blueprint("teams", __name__, url_prefix="/teams")


@teams_site.get("/")
def index():
    teams = Team.get_all()
    renderedteams = [t.to_dict() for t in teams]

    return render_template("spielleitung/teams/index.html",
                           back=url_for("site.spielleitung.index"),
                           teams=renderedteams)


@teams_site.route("/<int:team_id>/edit", methods=["GET", "POST"])
def edit(team_id):
    team = Team.get_via_id(team_id)

    form: EditTeamForm = EditTeamForm()

    if form.validate_on_submit():
        if form.delete.data:
            try:
                team.delete()
            except Exception as e:
                flash(str(e), "danger")
                return redirect(url_for(".edit", team_id=team.id))
            return redirect(url_for(".index"))

        if form.update.data:
            try:
                team.change_data(name=form.name.data)
            except Exception as e:
                flash(str(e), "danger")
                return redirect(url_for(".edit", team_id=team.id))
            return redirect(url_for(".index"))

    form.name.data = team.name if form.name.data is None else form.name.data

    return render_template("spielleitung/teams/edit.html",
                           back=url_for(".index"),
                           team=team.to_dict(),
                           form=form)
