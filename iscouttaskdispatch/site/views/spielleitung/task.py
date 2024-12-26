from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

from ....database.db import Status, Task, Team
from ....database.exceptions import ElementAlreadyExists, ElementDoesNotExsist
from ....tools import formatDatetime
from ...forms import EditTaskForm, NewTaskForm, ShowTaskForm

tasks_site = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_site.get("/")
def index():
    tasks = Task.get_all()
    return render_template("spielleitung/tasks/index.html",
                           tasks=[t.to_dict() for t in tasks])


@tasks_site.route("/<int:id>/show", methods=["GET", "POST"])
def show(id):
    task = Task.get_via_id(id)

    form: ShowTaskForm = ShowTaskForm()

    if form.failed.data and form.comment.data:
        task.update_data(status_id=4,
                         comment=form.comment.data,
                         updated_by="Spielleitung")
        print(task.comment)
        return redirect(url_for(".index"))

    if form.success.data:
        task.update_data(status_id=3, updated_by="Spielleitung")
        return redirect(url_for(".index"))

    form.comment.data = task.comment

    return render_template("spielleitung/tasks/show.html",
                           form=form,
                           task=task.to_dict(),
                           logs=str(task.log).split("\n"))


@tasks_site.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    task = Task.get_via_id(id)

    form: EditTaskForm = EditTaskForm()
    form.status.choices = [(-1, "Unverändert")] + \
        [(status.id, status.name) for status in Status.get_all()]
    form.team.choices = [(-1, "Unverändert")] + \
        [(team.id, f"#{team.id}: {team.name}") for team in Team.get_all()]

    print(request.form)
    if form.validate_on_submit():
        if form.delete.data:
            task.delete()
            return redirect(url_for(".index"))

        newStatus = form.status.data if int(form.status.data) != -1 else None

        task.update_data(name=form.name.data,
                         description=form.description.data,
                         comment=form.comment.data,
                         link=form.link.data,
                         status_id=newStatus,
                         format=form.format.data,
                         updated_by="Spielleitung")

        if int(form.team.data) != -1:
            team = Team.get_via_id(int(form.team.data))
            task.assign_to_team(team, True)

        return redirect(url_for(".index"))

    form.name.data = task.name
    form.description.data = task.description
    form.comment.data = task.comment
    form.link.data = task.link
    # form.status.data = task.status_id  # Wert soll nicht geändert werden um versehentliche Änderungen zu vermeiden
    form.format.data = task.format

    form.update_form()
    return render_template("spielleitung/tasks/edit.html",
                           form=form,
                           task=task,
                           logs=str(task.log).split("\n"))


@tasks_site.route("/create", methods=["GET", "POST"])
def create():
    form: NewTaskForm = NewTaskForm()

    if form.validate_on_submit():
        try:
            Task.create_new(id=form.taskID.data,
                            name=form.name.data,
                            description=form.description.data,
                            comment=form.comment.data,
                            link=form.link.data,
                            format=form.format.data)
        except ElementAlreadyExists as e:
            form.taskID.errors.append(str(e))
        else:
            return redirect(url_for(".index"))

    return render_template("spielleitung/tasks/create.html", form=form)
