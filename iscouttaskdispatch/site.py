from datetime import datetime as dt
from datetime import date
from flask import request, Response, jsonify, Blueprint, redirect,flash,render_template,abort
from flask.helpers import url_for
from flask.templating import render_template
from sqlalchemy import desc
from pprint import pprint
from .database.handel import *
from .tools import formatDatetime 
from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import create_engine, MetaData

site = Blueprint("site", __name__, template_folder="templates")

@site.route("/")
def index():
    return render_template("index.html")

### TASKS

@site.route("/tasks")
def showAllTasks():
    teams = {i['teamID']:i['name'] for i in getAllTeams()}
    tasks = getAllTasks()
    for task in tasks:
        task['description'] = task['description'].replace("\r", "").replace("\n","<br>")
        task['teamName'] = teams[task['teamID']] if task['teamID'] != None else "Kein Team Ausgewählt"
        status = getStatusOfTask(task['taskID'])
        statusName = status['name']
        statusTimestampString : str = formatDatetime(status['timestamp'])
        task['status'] = statusName
        task['statustimestamp'] = statusTimestampString
    return render_template("task/index.html", tasks=tasks, teams=getAllTeams())


@site.route("/tasks/<int:taskID>/edit")
def editTask(taskID):
    task = getTaskViaID(taskID)
    status = getStatusOfTask(task['taskID'])
    task['status'] = status['name']
    return render_template("task/edit.html", task=task)


@site.route("/tasks/<int:taskID>/update", methods=["POST"])
def updateTask(taskID):
    print("UPDATING TASK")
    name = request.form.get("name")
    description = request.form.get("description")
    status = int(request.form.get("new_status"))
    task = getTaskViaID(taskID)
    if task['name'] != name or task['description'] != description or getStatusOfTask(taskID)['statusID'] != status:
        setTaskName(taskID, name)
        setTaskDescription(taskID, description)
        setTaskStatus(taskID, status, "set Status via UI")
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
            createTask(form_data["taskID"], form_data["name"], form_data["description"], "Created via UI")
            return redirect(url_for("site.showAllTasks"))
        except ElementAlreadyExists:
            error_message = "Task with the provided ID already exists."

    return render_template("task/create.html", error_message=error_message, form_data=form_data)


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

    return render_template("task/delete.html", error_message=error_message)


@site.route("/tasks/<int:taskID>/assign", methods=["POST"])
def assignTaskSite(taskID):
    teamID = request.form.get("team", type=int)
    assignTask(taskID, teamID)
    return redirect(url_for("site.showAllTasks"))


@site.route("/task")
def redirectToTasks():
    return redirect(url_for("site.Tasks"))


@site.route("/tasks/<taskID>")
def specificTask(taskID):
    teams = {i['teamID']:i['name'] for i in getAllTeams()}
    statuses = getAllStatusesOfTask(int(taskID))
    for status in statuses:
        status['timestamp'] = formatDatetime(status['timestamp'])
    task = getTaskViaID(taskID)
    task['description'] = task['description'].replace("\r", "").replace("\n","<br>")
    task['teamName'] = teams[task['teamID']] if task['teamID'] != None else "Kein Team Ausgewählt"
    return render_template("task/task.html", task=task, statuses=statuses)



### TEAMS

@site.route("/teams")
def showAllTeams():
    teams = getAllTeams()
    return render_template("team/index.html", teams=teams)

@site.route("/teams/create", methods=["GET", "POST"])
def createTeamSite():
    error_message = None
    form_data = {"teamID": None, "name": ""}

    if request.method == "POST":
        form_data["teamID"] = int(request.form.get("teamID"))
        form_data["name"] = request.form.get("name")

        try:
            createTeam(form_data["teamID"], form_data["name"])
            return redirect(url_for("site.showAllTeams"))
        except ElementAlreadyExists:
            error_message = "Team with the provided ID already exists."

    return render_template("team/create.html", error_message=error_message, form_data=form_data)

@site.route("/teams/delete", methods=["GET", "POST"])
def deleteTeamSite():
    error_message = None
    if request.method == "POST":
        teamID = int(request.form.get("teamID"))

        try:
            deleteTeam(teamID)
            return redirect(url_for("site.showAllTeams"))
        except ElementDoesNotExsist:
            error_message = "Team with the provided ID does not exists."
            # You can handle the error as needed, such as displaying a message to the user.

    return render_template("team/delete.html", error_message=error_message)


@site.route("/teams/<int:teamID>")
def showTeam(teamID):
    return render_template("team/team.html", team=getTeamViaID(teamID))


@site.route("/teams/<int:teamID>/edit")
def editTeam(teamID):
    team = getTaskViaID(teamID)
    return render_template("team/edit.html", team=team)
    


### OTHER

@site.route("/db/ta")
def dbTa():
    return getAllTasks()

@site.route("/db/tast")
def dbTast():
    return getAllTaskHasStatus()