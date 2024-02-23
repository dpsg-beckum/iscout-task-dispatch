from flask import render_template, request, abort, redirect, url_for
from ....database.handel import *
from ..tools import formatDatetime
from flask import Blueprint
import time
from datetime import datetime

player_site = Blueprint("player_site",
                        __name__,
                        template_folder="../templates",
                        url_prefix="/player")


@player_site.route("/")
def index():
    return getAllTeams()


@player_site.route("/<int:teamID>")
def showTeam(teamID):
    return get_tasks_with_latest_status_by_team(teamID)
