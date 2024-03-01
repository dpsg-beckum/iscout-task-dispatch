# site/views/task_views.py
from flask import render_template, request, redirect, url_for
from ....database.handel import *
from ....tools import formatDatetime
from flask import Blueprint
import time
from datetime import datetime

tasks_site = Blueprint("tasks_site", __name__, url_prefix="/tasks")

@tasks_site.route("/")
def index():
    current_time = datetime.now().strftime('%H:%M:%S')
    teams = {i['teamID']:i['name'] for i in getAllTeams()}
    tasks = getAllTasks()
    for task in tasks:
        task['description'] = task['description'].replace("\r", "").replace("\n","<br>")
        task['teamName'] = teams[task['teamID']] if task['teamID'] != None else "Kein Team Ausgewählt"
        status = getStatusOfTask(task['taskID'])
        task['status'] = status['name']
        task['statusText'] = status['text']
        task['statustimestamp'] = formatDatetime(status['timestamp'])
    return render_template("spielleitung/tasks/index.html", tasks=tasks, teams=getAllTeams())


@tasks_site.route("/<int:taskID>/edit")
def editTask(taskID):
    task = getTaskViaID(taskID)
    taskStatus = getStatusOfTask(task['taskID'])
    task['status'] = taskStatus['name']
    return render_template("spielleitung/tasks/edit.html", 
                           task=task,
                           statuses=[{"id": k , "name": v} for k,v in getAllStatuses().items()])


@tasks_site.route("/<int:taskID>/update", methods=["POST"])
def updateTask(taskID):
    name = request.form.get("name")
    description = request.form.get("description")
    status = int(request.form.get("new_status"))
    task = getTaskViaID(taskID)
    if task['name'] != name or task['description'] != description or getStatusOfTask(taskID)['statusID'] != status:
        setTaskName(taskID, name)
        setTaskDescription(taskID, description)
        setTaskStatus(taskID, status, "set Status via UI")
    return redirect(url_for(".index"))


@tasks_site.route("/create", methods=["GET", "POST"])
def createTaskSite():
    error_message = None
    form_data = {"taskID": None, "name": "", "description": ""}

    if request.method == "POST":
        form_data["taskID"] = int(str(request.form.get("taskID")))
        form_data["name"] = request.form.get("name").strip()
        form_data["description"] = request.form.get("description").strip()

        try:
            createTask(form_data["taskID"], form_data["name"], form_data["description"], "Created via UI")
            return redirect(url_for(".index"))
        except ElementAlreadyExists:
            error_message = "Task with the provided ID already exists."
        except Exception as ex:
            error_message = str(ex)

    return render_template("spielleitung/tasks/create.html", error_message=error_message, form_data=form_data)


@tasks_site.route("/<int:taskID>/delete", methods=["POST"])
def deleteTaskSite(taskID):
    error_message = None
    if request.method == "POST":
        try:
            deleteTask(taskID)
            return redirect(url_for(".index"))
        except ElementDoesNotExsist:
            error_message = "Task with the provided ID does not exists."
            # You can handle the error as needed, such as displaying a message to the user.

    return render_template("error.html", error_message=error_message)


@tasks_site.route("/<int:taskID>/assign", methods=["POST"])
def assignTaskSite(taskID):
    teamID = request.form.get("team", type=int)
    assignTask(taskID, teamID, "Assigned via WEB UI", override=True)
    return redirect(url_for(".index"))


@tasks_site.route("/<taskID>")
def specificTask(taskID):
    teams = {i['teamID']:i['name'] for i in getAllTeams()}
    statuses = getAllStatusesOfTask(int(taskID))
    for status in statuses:
        status['timestamp'] = formatDatetime(status['timestamp'])
    task = getTaskViaID(taskID)
    task['description'] = task['description'].replace("\r", "").replace("\n","<br>")
    task['teamName'] = teams[task['teamID']] if task['teamID'] != None else "Kein Team Ausgewählt"
    return render_template("spielleitung/tasks/task.html", task=task, statuses=statuses)
