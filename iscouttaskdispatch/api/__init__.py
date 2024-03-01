from flask import Blueprint, render_template, request, redirect, url_for, abort, jsonify
from ..database.handel import *

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/")
def index():
    return "OK"


@api.route("/task/create", methods=["POST"])
def createTaskApi():
    try:
        taskID = int(str(request.form.get("taskID")))
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()
        createTask(taskID, name, description, "Created via API")
        return "OK"
    except ValueError:
        return abort(400)
    except ElementAlreadyExists:
        abort(409,"Task with the provided ID already exists.")
    except Exception as ex:
        print(ex)
        abort(500, str(ex))
        
@api.route("/task/<int:taskID>/setstatus/<int:statusID>", methods=["GET", "POST"])
def work(taskID, statusID):
    setTaskStatus(taskID,statusID,"API")
    return "OK"

@api.route("/data")
def getGeneralData():
    teams = {i['teamID']:i['name'] for i in getAllTeams()}
    tasks = getAllTasks()

    allStatuses = getAllStatuses()
    values = [0 for i in range(len(allStatuses.keys()))]
    statuses = [v for k,v in allStatuses.items()]

    for task in tasks:
        task['description'] = convert_text_to_links(task['description'])
        task['teamName'] = teams[task['teamID']] if task['teamID'] != None else "Kein Team Ausgewählt"
        status = getStatusOfTask(task['taskID'])
        task['statusID'] = status['statusID']
        task['status'] = status['name']
        task['statusText'] = status['text']
        task['statustimestamp'] = formatDatetime(status['timestamp'])

        key = getStatusOfTask(task['taskID'])['statusID'] -1
        if key != -1:
            values[key] += 1
    
    piechart = {'values': values, 'labels': statuses}
    
    out = {"piechart": piechart,
           "tasks": tasks,
           "statuses": getAllStatuses()}
    
    return jsonify(out)