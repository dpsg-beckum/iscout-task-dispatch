from flask import render_template, request, abort, redirect, url_for
from ....database.handel import *
from ..tools import formatDatetime
from flask import Blueprint
import time
from datetime import datetime

player_site = Blueprint("player_site", __name__, url_prefix="/player")


@player_site.route("/")
def index():
    teams = getAllTeams()
    return render_template("player/index.html", teams=teams)


@player_site.route("/<int:teamID>")
def overview(teamID):
    team = getTeamViaID(teamID)
    tasks = get_tasks_with_latest_status_by_team(teamID)
    return render_template("player/overview.html",
                           team=team,
                           tasks=[i for i in tasks if i['statusID'] == 3])
    
    
@player_site.route("/<int:teamID>/leader")
def leader(teamID):
    team = getTeamViaID(teamID)
    tasks = get_tasks_with_latest_status_by_team(teamID)
    return render_template("player/leader.html",
                           team=team,
                           failed_tasks=[i for i in tasks if i['statusID'] == 5],
                           wip_task=[i for i in tasks if i['statusID'] == 3],
                           assigned_task=[i for i in tasks if i['statusID'] <= 2],
                           available_tasks=get_tasks_with_latest_status_by_team(None))

