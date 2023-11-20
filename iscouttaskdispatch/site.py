from datetime import datetime as dt
from datetime import date
from flask import request, Response, jsonify, Blueprint, redirect,flash,render_template
from flask.helpers import url_for
from flask.templating import render_template
from sqlalchemy import desc
from pprint import pprint
from .database.handel import *


site = Blueprint("site", __name__, template_folder="templates")

@site.route("/")
def index():
    return render_template("index.html")

@site.route("/tasks")
def showAllTasks():
    tasks = getAllTasks()
    for task in tasks:
        task['description'] = task['description'].replace("\r", "").replace("\n","<br>")
    return render_template("tasks.html", tasks=tasks)

@site.route("/tasks/<int:taskID>/edit")
def editTask(taskID):
    task = getTaskViaID(taskID)
    return render_template("edit_task.html", task=task)

@site.route("/tasks/<int:taskID>/update", methods=["POST"])
def updateTask(taskID):
    name = request.form.get("name")
    description = request.form.get("description")

    setTaskName(taskID, name)
    setTaskDescription(taskID, description)

    return redirect(url_for("site.showAllTasks"))

@site.route("/tasks/create", methods=["GET", "POST"])
def createTaskSite():
    error_message = None
    form_data = {"taskID": None, "name": "", "description": ""}

    if request.method == "POST":
        form_data["taskID"] = int(request.form.get("taskID"))
        form_data["name"] = request.form.get("name")
        form_data["description"] = request.form.get("description")

        try:
            createTask(form_data["taskID"], form_data["name"], form_data["description"])
            return redirect(url_for("site.showAllTasks"))
        except ElementAlreadyExists:
            error_message = "Task with the provided ID already exists."

    return render_template("create_task.html", error_message=error_message, form_data=form_data)

@site.route("/tasks/delete", methods=["GET", "POST"])
def deleteTaskSite():
    error_message = None
    if request.method == "POST":
        taskID = int(request.form.get("taskID"))

        try:
            deleteTask(taskID)
            return redirect(url_for("site.showAllTasks"))
        except ElementDoesNotExsist:
            error_message = "Task with the provided ID does not exists."
            # You can handle the error as needed, such as displaying a message to the user.

    return render_template("delete_task.html", error_message=error_message)