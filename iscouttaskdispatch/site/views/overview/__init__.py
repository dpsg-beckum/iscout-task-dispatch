# site/views/overview.py
from flask import render_template, request, redirect, url_for, jsonify, abort
from ....database.handel import *
from ....database.json_encoder import JSONEncoder
from ....tools import formatDatetime, convert_text_to_links
from flask import Blueprint
from pprint import pprint
import time
from datetime import datetime


overview_site = Blueprint("overview_site", __name__, url_prefix="/overview")


@overview_site.route("/")
def index():
    
    

    return render_template("overview/index.html")

@overview_site.route("/data")
def data():
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