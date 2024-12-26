import time
from datetime import datetime
from pprint import pprint

from flask import Blueprint, abort, redirect, render_template, request, url_for

from ....database.db import Task, Team
from ....tools import formatDatetime
from ...forms import NewTeamForm
from .team import id_site

teams_site = Blueprint("team", __name__, url_prefix="/teams")

teams_site.register_blueprint(id_site)


@teams_site.route("/")
def index():
    return redirect(url_for(".new"))


@teams_site.route("/new", methods=["GET", "POST"])
def new():
    form: NewTeamForm = NewTeamForm()

    if form.validate_on_submit():
        try:
            team = Team.create_new(form.name.data)
        except Exception as e:
            form.name.errors.append(str(e))
        else:
            return redirect(url_for(".id.overview", id=team.id))
    return render_template("team/new.html", form=form)
