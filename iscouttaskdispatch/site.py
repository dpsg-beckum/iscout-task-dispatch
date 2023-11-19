from datetime import datetime as dt
from datetime import date
from flask import request, Response, jsonify, Blueprint
from flask.helpers import url_for
from flask.templating import render_template
from sqlalchemy import desc
from .database.db import Team, Task, TaskHasStatus, Status
from pprint import pprint


site = Blueprint("site", __name__, template_folder="templates")

@site.route("/")
def helloWorld():
    status = Status.query.all()
    teams = Team.query.all()

    stat : Status
    for stat in status:
        print(stat.name)

    return render_template('helloworld.html')
